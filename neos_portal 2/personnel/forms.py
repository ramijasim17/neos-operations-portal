from django import forms
from .models import Personnel


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ["full_name", "employee_id", "position", "phone", "email", "active"]
