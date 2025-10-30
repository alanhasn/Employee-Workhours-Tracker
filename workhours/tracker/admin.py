from django.contrib import admin
from .models import Employee, WorkEntry


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ("name", "position", "created_at")
	search_fields = ("name", "position")


@admin.register(WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
	list_display = ("employee", "date", "start_time", "end_time", "duration_hours")
	list_filter = ("employee", "date")
	search_fields = ("employee__name",)
	date_hierarchy = "date"


