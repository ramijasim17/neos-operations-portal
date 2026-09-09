from django.contrib import admin
from .models import SQBJob, SQBDocument


class SQBDocumentInline(admin.TabularInline):
    model = SQBDocument
    extra = 0


@admin.register(SQBJob)
class SQBJobAdmin(admin.ModelAdmin):
    list_display = ("job_number", "job_name", "permit_number", "created_at")
    inlines = [SQBDocumentInline]
