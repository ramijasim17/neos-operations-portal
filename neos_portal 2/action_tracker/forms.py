from django import forms
from .models import ActionItem


class ActionItemForm(forms.ModelForm):
    steps_text = forms.CharField(
        widget=forms.Textarea, required=False,
        label="Steps (one per line, optional)",
        help_text="Only used when creating a new action.",
    )

    class Meta:
        model = ActionItem
        fields = ["action_item", "assignee", "priority", "due_date", "comments"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}
