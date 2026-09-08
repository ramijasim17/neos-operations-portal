from django import forms
from .models import MaintenanceRecord


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ["equipment", "level", "due_date", "file"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
