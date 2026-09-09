from django.contrib import admin
from .models import ActionItem, ActionStep


class ActionStepInline(admin.TabularInline):
    model = ActionStep
    extra = 1


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ("action_item", "assignee", "priority", "status", "due_date")
    list_filter = ("status", "priority")
    inlines = [ActionStepInline]
