from django.contrib import admin
from .models import Personnel


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("full_name", "employee_id", "position", "phone", "active")
    list_filter = ("position", "active")
    search_fields = ("full_name", "employee_id")
