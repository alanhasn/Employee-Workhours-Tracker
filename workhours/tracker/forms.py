from django import forms
from django.utils import timezone
from .models import WorkEntry, Employee


class WorkEntryForm(forms.ModelForm):
	class Meta:
		model = WorkEntry
		fields = ["employee", "date", "start_time", "end_time", "extra_hours"]
		widgets = {
			"employee": forms.Select(attrs={
				"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
			}),
			"date": forms.DateInput(attrs={
				"type": "date",
				"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
			}),
			"start_time": forms.TimeInput(attrs={
				"type": "time",
				"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
			}),
			"end_time": forms.TimeInput(attrs={
				"type": "time",
				"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
			}),
			"extra_hours": forms.NumberInput(attrs={
				"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
				"step": "0.5"
			}),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Only set initial values if this is a new form (no instance)
		if not self.instance.pk:
			now = timezone.localtime()
			self.fields['date'].initial = now.date()
			self.fields['start_time'].initial = now.strftime('%H:%M')
			# Set default end time to 3:30 PM
			self.fields['end_time'].initial = '15:30'


class FilterForm(forms.Form):
	employee = forms.ModelChoiceField(
		queryset=Employee.objects.all(),
		required=False,
		widget=forms.Select(attrs={
			"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
		})
	)
	start_date = forms.DateField(
		required=False,
		widget=forms.DateInput(attrs={
			"type": "date",
			"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
		})
	)
	end_date = forms.DateField(
		required=False,
		widget=forms.DateInput(attrs={
			"type": "date",
			"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
		})
	)
	year = forms.IntegerField(
		required=False,
		min_value=1970,
		max_value=2100,
		widget=forms.NumberInput(attrs={
			"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
		})
	)
	month = forms.IntegerField(
		required=False,
		min_value=1,
		max_value=12,
		widget=forms.NumberInput(attrs={
			"class": "bg-dark-700 border-dark-600 text-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
		})
	)


