from django.db import models
from django.conf import settings
# Create your models here.

class FormSubmission(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'submitted','Submitted'
        ACKNOWLEDED = 'acknowledged','Acknowledged'
        RETURNED = 'returned', 'Returned'
 
    
    FORM_TYPE_CHOICES = [
        ('Learner Onboarding Form', 'Learner Onboarding Form'),
        ('Session Outline', 'Session Outline'),
        ('Progress Report', 'Progress Report'),
        ('General Submission', 'General Submission'),
    ]

    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    department = models.ForeignKey('core.Department', on_delete=models.PROTECT)
    form_type = models.CharField(max_length=100, choices=FORM_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    attachment = models.FileField(upload_to='submissions/%Y/%m/', blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SUBMITTED)
    supervisor_note = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
