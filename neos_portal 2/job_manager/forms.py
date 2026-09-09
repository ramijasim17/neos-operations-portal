from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["job_name", "client", "date", "equipment_list"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
