from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None ,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email, password,**extra_fields)
    
class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERVISOR ='supervisor','Supervisor'
        INSTRUCTOR = 'instructor','Instructor'

    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=Role.choices,blank=True)
    department = models.ForeignKey(
        'core.Department',
        on_delete=models.PROTECT,
        null= True,
        blank=True,
    )    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__ (self):
        return self.name or self.email