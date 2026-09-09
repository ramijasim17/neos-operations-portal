from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("job_name", "client", "date")
    search_fields = ("job_name", "client")
