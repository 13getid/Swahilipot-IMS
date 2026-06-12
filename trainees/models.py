from django.db import models
from django.conf import settings


# Create your models here.
class Trainee(models.Model):
    name = models.CharField(max_length=150)
    phone= models.CharField(max_length=20)
    department = models.ForeignKey('core.Department',on_delete=models.PROTECT)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
      return self.name

