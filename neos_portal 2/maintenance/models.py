"""
maintenance/models.py — Django equivalent of tab_maintenance.py.
Every record links to an actual Equipment row (from the equipment app),
same as the Streamlit version required picking real equipment from a
dropdown rather than typing a serial number freehand.
"""

from datetime import date, timedelta

from django.conf import settings
from django.db import models

from equipment.models import Equipment


class MaintenanceLevel(models.Model):
    """Extensible list, same idea as CertType — managed from admin/Settings
    rather than hardcoded, seeded with common defaults on first use."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


DEFAULT_LEVELS = ["Level 1", "Level 2", "Level 3", "Level 4", "Overhaul"]


def maintenance_upload_path(instance, filename):
    return f"maintenance/{instance.equipment.serial_number}/{filename}"


class MaintenanceRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="maintenance_records")
    level = models.ForeignKey(MaintenanceLevel, on_delete=models.PROTECT)
    due_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=maintenance_upload_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.equipment.serial_number} · {self.level.name}"

    @property
    def status(self) -> str:
        """overdue / soon / scheduled / na — same bucket logic as everywhere
        else in the app (common.py's status_bucket_from_date in Streamlit)."""
        if not self.due_date:
            return "na"
        today = date.today()
        if self.due_date < today:
            return "expired"
        if self.due_date <= today + timedelta(days=30):
            return "soon"
        return "valid"
