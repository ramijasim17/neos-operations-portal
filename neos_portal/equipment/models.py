"""
equipment/models.py — mirrors the equipment / equipment_certs / cert_types /
category_cert_map tables from your Streamlit app's Turso database.

Django's ORM replaces raw SQL here: instead of `db.execute("CREATE TABLE...")`
in migrations.py, you define models and run `python manage.py makemigrations`
+ `migrate` — Django writes and tracks the SQL for you, including future
schema changes, which used to be manual ALTER TABLE calls.
"""

from django.db import models
from django.conf import settings


class Category(models.TextChoices):
    UNITS = "Units", "Units"
    PCE = "PCE", "PCE"
    DOWN_HOLE_TOOLS = "Down Hole Tools", "Down Hole Tools"
    FLANGE = "Flange", "Flange"
    CROSSOVER = "Crossover", "Crossover"
    SAFETY_DEVICE = "Safety Device", "Safety Device"
    LIFTING_GEARS = "Lifting Gears", "Lifting Gears"
    INSTRUMENT = "Instrument", "Instrument"


class CertType(models.Model):
    """Equivalent of the cert_types table — an extensible list of
    certificate type names, managed from Settings rather than hardcoded."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CategoryCertRequirement(models.Model):
    """Equivalent of category_cert_map — which cert types are required for
    which equipment category."""
    category = models.CharField(max_length=50, choices=Category.choices)
    cert_type = models.ForeignKey(CertType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("category", "cert_type")


class Equipment(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=Category.choices)
    description = models.CharField(max_length=255, blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        ordering = ["category", "serial_number"]
        verbose_name_plural = "Equipment"

    def __str__(self):
        return f"{self.serial_number} ({self.category})"

    def required_cert_types(self):
        return CertType.objects.filter(categorycertrequirement__category=self.category)


def cert_upload_path(instance, filename):
    """Files land under equipment_certs/<serial_number>/<cert_type>/<filename>
    in the object storage bucket — the S3 equivalent of the
    Equipment_Certificates/<subfolder> structure used in Google Drive."""
    return f"equipment_certs/{instance.equipment.serial_number}/{instance.cert_type.name}/{filename}"


class EquipmentCert(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="certs")
    cert_type = models.ForeignKey(CertType, on_delete=models.CASCADE)
    cert_number = models.CharField(max_length=100, blank=True, default="")
    expiry_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=cert_upload_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Who uploaded/last replaced this file — an audit trail your Streamlit app didn't have.",
    )

    class Meta:
        unique_together = ("equipment", "cert_type")

    def __str__(self):
        return f"{self.equipment.serial_number} · {self.cert_type.name}"

    @property
    def status(self) -> str:
        """expired / soon / valid / missing — same bucket logic as common.py's
        status_bucket_from_date() in the Streamlit app, kept consistent."""
        if not self.file:
            return "missing"
        if not self.expiry_date:
            return "na"
        from datetime import date, timedelta
        today = date.today()
        if self.expiry_date < today:
            return "expired"
        if self.expiry_date <= today + timedelta(days=30):
            return "soon"
        return "valid"
