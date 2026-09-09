from django.conf import settings
from django.db import models


class Priority(models.TextChoices):
    HIGH = "High", "High"
    MEDIUM = "Medium", "Medium"
    LOW = "Low", "Low"


class Status(models.TextChoices):
    PENDING = "Pending", "Pending"
    IN_PROGRESS = "In Progress", "In Progress"
    COMPLETED = "Completed", "Completed"


class ActionItem(models.Model):
    action_item = models.CharField(max_length=255)
    assignee = models.CharField(max_length=150, blank=True, default="")
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    comments = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["status", "due_date"]

    def __str__(self):
        return self.action_item

    @property
    def progress(self):
        steps = self.steps.all()
        total = steps.count()
        done = steps.filter(is_completed=True).count()
        return done, total


class ActionStep(models.Model):
    action = models.ForeignKey(ActionItem, on_delete=models.CASCADE, related_name="steps")
    step_description = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.step_description
