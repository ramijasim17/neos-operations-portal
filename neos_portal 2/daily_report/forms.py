from django import forms
from .models import DailyReport


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ["date", "job_name", "daily_link", "prejob_link", "postjob_link"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
