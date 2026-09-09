from django.db import models


class DailyReport(models.Model):
    """Mirrors the original daily_reports table from app.py's inline schema:
    date, job_name, daily_link, prejob_link, postjob_link. These are links
    (e.g. to a Drive doc or shared report), not file uploads."""
    date = models.DateField()
    job_name = models.CharField(max_length=255)
    daily_link = models.URLField(blank=True, default="")
    prejob_link = models.URLField(blank=True, default="")
    postjob_link = models.URLField(blank=True, default="")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.job_name} ({self.date})"
