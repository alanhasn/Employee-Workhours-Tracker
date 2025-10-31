from __future__ import annotations

from datetime import date as date_cls
from calendar import monthrange

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from typing import Any

from django.contrib.auth.views import LoginView, LogoutView

from .forms import WorkEntryForm, FilterForm
from .models import Employee, WorkEntry


class AdminLoginView(View):
    """
    Custom login view for admin users only.
    Renders and handles login on the same page.
    """

    template_name = "tracker/login.html"
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        # If already logged in, redirect to dashboard
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(reverse("dashboard"))
        
        form = self.form_class(request)
        next_url = request.GET.get("next", "")
        return render(request, self.template_name, {"form": form, "next": next_url})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        next_url = request.POST.get("next") or reverse("dashboard")

        if form.is_valid():
            user = form.get_user()

            if not (user.is_active and user.is_staff):
                form.add_error(None, "You do not have permission to access the admin area.")
                return render(request, self.template_name, {"form": form, "next": next_url})

            login(request, user)
            return redirect(next_url)

        # Re-render same page with form errors
        return render(request, self.template_name, {"form": form, "next": next_url})
    

class DashboardView(LoginRequiredMixin, View):
    login_url = '/app/'
    redirect_field_name = 'next'
    
    def get(self, request):
        form = FilterForm(request.GET or None)
        entries = WorkEntry.objects.select_related("employee").all()

        # Filtering
        if form.is_valid():
            employee = form.cleaned_data.get("employee")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            year = form.cleaned_data.get("year")
            month = form.cleaned_data.get("month")

            if employee:
                entries = entries.filter(employee=employee)
            if start_date:
                entries = entries.filter(date__gte=start_date)
            if end_date:
                entries = entries.filter(date__lte=end_date)
            if year:
                entries = entries.filter(date__year=year)
            if month:
                entries = entries.filter(date__month=month)

        elif request.GET:
            # If invalid GET params, still show something reasonable
            form = FilterForm()

        # Aggregations
        total_hours_overall = entries.aggregate(total=Sum("duration_hours"))["total"] or 0

        # Per employee per month/year
        year_for_summary = form.cleaned_data.get("year") if form.is_valid() else date_cls.today().year
        month_for_summary = form.cleaned_data.get("month") if form.is_valid() else date_cls.today().month

        monthly = (
            WorkEntry.objects.filter(date__year=year_for_summary, date__month=month_for_summary)
            .values("employee__id", "employee__name")
            .annotate(total=Sum("duration_hours"))
            .order_by("employee__name")
        )

        yearly = (
            WorkEntry.objects.filter(date__year=year_for_summary)
            .values("employee__id", "employee__name")
            .annotate(total=Sum("duration_hours"))
            .order_by("employee__name")
        )

        context = {
            "form": form,
            "entries": entries.order_by("-date", "-start_time")[:500],
            "total_hours_overall": total_hours_overall,
            "monthly": monthly,
            "yearly": yearly,
            "summary_year": year_for_summary,
            "summary_month": month_for_summary,
        }

        return render(request, "tracker/dashboard.html", context)


class WorkEntryListView(LoginRequiredMixin, View):
    login_url = '/app/'
    redirect_field_name = 'next'
    def get(self, request):
        entries = WorkEntry.objects.select_related("employee").order_by("-date", "-start_time")
        return render(request, "tracker/workentry_list.html", {"entries": entries})


class WorkEntryCreateView(LoginRequiredMixin, View):
    login_url = '/app/'
    redirect_field_name = 'next'
    def get(self, request):
        form = WorkEntryForm()
        return render(request, "tracker/workentry_form.html", {"form": form, "title": "Add Work Entry"})

    def post(self, request):
        form = WorkEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("dashboard"))
        return render(request, "tracker/workentry_form.html", {"form": form, "title": "Add Work Entry"})


class WorkEntryUpdateView(LoginRequiredMixin, View):
    login_url = '/app/'
    redirect_field_name = 'next'
    def get(self, request, pk: int):
        entry = get_object_or_404(WorkEntry, pk=pk)
        form = WorkEntryForm(instance=entry)
        return render(request, "tracker/workentry_form.html", {"form": form, "title": "Edit Work Entry"})

    def post(self, request, pk: int):
        entry = get_object_or_404(WorkEntry, pk=pk)
        form = WorkEntryForm(request.POST, instance=entry)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse("workentry_list"))
            except Exception as e:
                form.add_error(None, f"Error saving entry: {str(e)}")
        return render(request, "tracker/workentry_form.html", {
            "form": form,
            "title": "Edit Work Entry",
            "entry": entry
        })


class WorkEntryDeleteView(LoginRequiredMixin, View):
    login_url = '/app/'
    redirect_field_name = 'next'
    def get(self, request, pk: int):
        entry = get_object_or_404(WorkEntry, pk=pk)
        return render(request, "tracker/confirm_delete.html", {"object": entry, "title": "Delete Work Entry"})

    def post(self, request, pk: int):
        entry = get_object_or_404(WorkEntry, pk=pk)
        entry.delete()
        return redirect(reverse("workentry_list"))


class EmployeeListView(LoginRequiredMixin, View):
    login_url = '/app/'
    redirect_field_name = 'next'
    def get(self, request):
        employees = Employee.objects.all().order_by("name")
        return render(request, "tracker/employee_list.html", {"employees": employees})


class AnalyticsView(LoginRequiredMixin, View):
    login_url = '/app/'
    redirect_field_name = 'next'
    def get(self, request):
        today = date_cls.today()
        current_year = today.year
        current_month = today.month
        current_month_str = today.strftime("%Y-%m")

        # Monthly totals per employee
        monthly_totals = (
            WorkEntry.objects.filter(date__year=current_year, date__month=current_month)
            .values("employee__name")
            .annotate(
                regular_hours=Sum("duration_hours"),
                extra_hours=Sum("extra_hours"),
                total_hours=Sum("total_hours"),
            )
            .order_by("employee__name")
        )

        # Monthly total
        monthly_total = WorkEntry.objects.filter(
            date__year=current_year, date__month=current_month
        ).aggregate(
            regular_hours=Sum("duration_hours"),
            extra_hours=Sum("extra_hours"),
            total_hours=Sum("total_hours"),
        )

        # Yearly totals per employee
        yearly_totals = (
            WorkEntry.objects.filter(date__year=current_year)
            .values("employee__name")
            .annotate(
                regular_hours=Sum("duration_hours"),
                extra_hours=Sum("extra_hours"),
                total_hours=Sum("total_hours"),
            )
            .order_by("employee__name")
        )

        # Yearly total
        yearly_total = WorkEntry.objects.filter(date__year=current_year).aggregate(
            regular_hours=Sum("duration_hours"),
            extra_hours=Sum("extra_hours"),
            total_hours=Sum("total_hours"),
        )

        context = {
            "current_year": current_year,
            "current_month_str": current_month_str,
            "monthly_totals": monthly_totals,
            "monthly_total": monthly_total,
            "yearly_totals": yearly_totals,
            "yearly_total": yearly_total,
        }

        return render(request, "tracker/analytics.html", context)
