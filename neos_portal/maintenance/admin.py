from django.contrib import admin
from .models import MaintenanceLevel, MaintenanceRecord


@admin.register(MaintenanceLevel)
class MaintenanceLevelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("equipment", "level", "due_date", "status", "uploaded_by", "uploaded_at")
    list_filter = ("level",)
    search_fields = ("equipment__serial_number",)
