from datetime import date, timedelta
from django.conf import settings
from django.db import models

DEFAULT_TYPES = ["SOC", "Work Approval"]


class FileType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


def wa_upload_path(instance, filename):
    return f"work_approval/{instance.file_type.name}/{filename}"


class ApprovalRecord(models.Model):
    file_type = models.ForeignKey(FileType, on_delete=models.PROTECT)
    expiry_date = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True, default="")
    file = models.FileField(upload_to=wa_upload_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["expiry_date"]

    def __str__(self):
        return f"{self.file_type.name} ({self.expiry_date})"

    @property
    def status(self) -> str:
        if not self.expiry_date:
            return "na"
        today = date.today()
        if self.expiry_date < today:
            return "expired"
        if self.expiry_date <= today + timedelta(days=30):
            return "soon"
        return "valid"
