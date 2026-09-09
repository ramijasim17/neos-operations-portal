from django import forms
from .models import ApprovalRecord


class ApprovalRecordForm(forms.ModelForm):
    class Meta:
        model = ApprovalRecord
        fields = ["file_type", "expiry_date", "details", "file"]
        widgets = {"expiry_date": forms.DateInput(attrs={"type": "date"})}
