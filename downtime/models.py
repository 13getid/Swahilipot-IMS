from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class DowntimeReport(models.Model):
    class Severity(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        RESOLVED = 'resolved', 'Resolved'

    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    frequency_band = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=Severity.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    resolution_note = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.frequency_band} ({self.severity})'