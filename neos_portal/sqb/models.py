from django.conf import settings
from django.db import models

SQB_DOCUMENT_TYPES = [
    "SL Unit Pre/Post Trip Inspection",
    "Trailer Safety Inspection Checklist",
    "Truck Mounted C-Line Crane Checklist",
    "Shift Hand-Over Checklist",
    "Pre Job-Briefing",
    "Toolbox Talk",
    "Toolbox Talk - SIMOPS TBT",
    "Crane Dropped Objects Inspection",
    "Slick Line Job Safety Analysis",
    "Full Body Harness Safety Inspection Checklist",
    "SLS Grounding Checklist",
    "E-STOP Daily Checklist",
    "Lifting Plan Form",
    "Pressure Awareness Checklist",
    "BOP Function Test at Wellsite Register",
    "Well Status Document (Pre-Job)",
    "SL Operation Pre Job-Rig Up Checklist",
    "Z-Chart Form",
    "Well Status Document (Post-Job)",
]


class SQBJob(models.Model):
    job_number = models.CharField(max_length=100, unique=True)
    job_name = models.CharField(max_length=255, blank=True, default="")
    permit_number = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.job_number

    def progress(self):
        uploaded = self.documents.exclude(file="").count()
        return uploaded, len(SQB_DOCUMENT_TYPES)


def sqb_upload_path(instance, filename):
    return f"sqb/{instance.job.job_number}/{instance.doc_type}/{filename}"


class SQBDocument(models.Model):
    job = models.ForeignKey(SQBJob, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=100)
    file = models.FileField(upload_to=sqb_upload_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("job", "doc_type")

    def __str__(self):
        return f"{self.job.job_number} · {self.doc_type}"
