
from django.db import models
from django.conf import settings
from django.utils import timezone

import uuid
from datetime import timedelta

# Create your models here.
def default_expiry():
    return timezone.now() + timedelta(hours=3)

class AttendanceSession(models.Model):
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    department = models.ForeignKey('core.Department', on_delete=models.PROTECT)
    token = models.UUIDField(default=uuid.uuid4, unique=False)
    session_label = models.CharField(max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    @property
    def is_expired(self):
        return self.expires_at< timezone.now()
    
    def __str__(self):
        return self.session_label or f'Session{self.id}'
    
class AttendanceRecord(models.Model):
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE,related_name='records')
    trainee_name = models.CharField(max_length=150)
    trainee_phone = models.CharField(max_length=20)
    tasks_completed = models.TextField()
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
      return self.trainee_name