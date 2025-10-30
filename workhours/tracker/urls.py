from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
	DashboardView,
	WorkEntryCreateView,
	WorkEntryListView,
	WorkEntryUpdateView,
	WorkEntryDeleteView,
	EmployeeListView,
	AnalyticsView,
	AdminLoginView,
)

urlpatterns = [
	path("", AdminLoginView.as_view(), name="login"),
	path("logout/", LogoutView.as_view(http_method_names=['get', 'post'], next_page="/app/"), name="logout"),
	path("dashboard/", DashboardView.as_view(), name="dashboard"),
	path("entries/", WorkEntryListView.as_view(), name="workentry_list"),
	path("entries/add/", WorkEntryCreateView.as_view(), name="workentry_add"),
	path("entries/<int:pk>/edit/", WorkEntryUpdateView.as_view(), name="workentry_edit"),
	path("entries/<int:pk>/delete/", WorkEntryDeleteView.as_view(), name="workentry_delete"),
	path("employees/", EmployeeListView.as_view(), name="employee_list"),
	path("analytics/", AnalyticsView.as_view(), name="analytics"),
]


