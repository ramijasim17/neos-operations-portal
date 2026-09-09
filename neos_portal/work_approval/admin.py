from django.contrib import admin
from .models import FileType, ApprovalRecord


@admin.register(FileType)
class FileTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ApprovalRecord)
class ApprovalRecordAdmin(admin.ModelAdmin):
    list_display = ("file_type", "expiry_date", "status", "uploaded_by", "uploaded_at")
    list_filter = ("file_type",)
