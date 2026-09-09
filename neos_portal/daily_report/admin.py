from django.contrib import admin
from .models import DailyReport


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ("job_name", "date")
    search_fields = ("job_name",)
