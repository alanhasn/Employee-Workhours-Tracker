from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError


class Employee(models.Model):
	name = models.CharField(max_length=255)
	position = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name


class WorkEntry(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="work_entries")
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	extra_hours = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal("0.00"), help_text="Additional work hours not covered by start/end time")
	# Store computed hours as Decimal for accuracy (e.g., 7.50 hours)
	duration_hours = models.DecimalField(max_digits=6, decimal_places=2, editable=False, default=Decimal("0.00"))
	total_hours = models.DecimalField(max_digits=6, decimal_places=2, editable=False, default=Decimal("0.00"))
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-date", "-start_time"]
		unique_together = ("employee", "date", "start_time", "end_time")

	def clean(self) -> None:
		if not all([self.date, self.start_time, self.end_time]):
			return

		start_dt = datetime.combine(self.date, self.start_time)
		end_dt = datetime.combine(self.date, self.end_time)
		
		# Handle case where end time is on the next day (crossing midnight)
		if self.end_time < self.start_time:
			end_dt = end_dt + timedelta(days=1)
		
		# Calculate duration
		delta: timedelta = end_dt - start_dt
		hours = Decimal(delta.total_seconds()) / Decimal(3600)
		
		# Round hours to 2 decimal places for comparison
		rounded_hours = hours.quantize(Decimal("0.01"))
		
		# Validate work duration
		if rounded_hours > 12:
			raise ValidationError("Work duration cannot exceed 12 hours per day. Current duration: {} hours".format(rounded_hours))
		elif rounded_hours <= 0:
			raise ValidationError("End time must be after start time.")

	def save(self, *args, **kwargs):
		self.full_clean()
		
		start_dt = datetime.combine(self.date, self.start_time)
		end_dt = datetime.combine(self.date, self.end_time)
		
		# Handle case where end time is on the next day
		if self.end_time < self.start_time:
			end_dt = end_dt + timedelta(days=1)
		
		delta: timedelta = end_dt - start_dt
		# Calculate hours with high precision
		hours = Decimal(str(delta.total_seconds())) / Decimal("3600")
		# Round to 2 decimal places for storage
		self.duration_hours = hours.quantize(Decimal("0.01"), rounding='ROUND_HALF_UP')
		# Add extra hours to get total
		self.total_hours = (self.duration_hours + self.extra_hours).quantize(Decimal("0.01"), rounding='ROUND_HALF_UP')
		return super().save(*args, **kwargs)

	def __str__(self) -> str:
		return f"{self.employee.name} - {self.date} ({self.duration_hours}h)"


