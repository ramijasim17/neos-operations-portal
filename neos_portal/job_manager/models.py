from django.db import models


class Job(models.Model):
    """Mirrors the original job_manifests table from app.py's inline schema:
    job_name, client, date, equipment_list."""
    job_name = models.CharField(max_length=255)
    client = models.CharField(max_length=255, blank=True, default="")
    date = models.DateField(null=True, blank=True)
    equipment_list = models.TextField(
        blank=True, default="",
        help_text="Equipment used on this job (free text list).",
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.job_name
