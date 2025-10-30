from __future__ import annotations

from datetime import date, time, timedelta
from random import randint

from django.core.management.base import BaseCommand

from tracker.models import Employee, WorkEntry


class Command(BaseCommand):
	help = "Seed database with example employees and work entries"

	def handle(self, *args, **options):
		# Create employees
		employees = [
			("Alice Johnson", "Engineer"),
			("Bob Smith", "Designer"),
			("Carol Lee", "Project Manager"),
		]
		created_employees = []
		for name, position in employees:
			e, _ = Employee.objects.get_or_create(name=name, defaults={"position": position})
			created_employees.append(e)

		# Create last 7 days of entries per employee
		for e in created_employees:
			for days_ago in range(1, 8):
				d = date.today() - timedelta(days=days_ago)
				start_hour = randint(8, 10)
				end_hour = start_hour + randint(6, 9)
				try:
					WorkEntry.objects.get_or_create(
						employee=e,
						date=d,
						start_time=time(start_hour, 0),
						end_time=time(min(end_hour, 23), 0),
					)
				except Exception:
					continue

		self.stdout.write(self.style.SUCCESS("Seed data created."))


