from django.contrib import admin
from .models import Department

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name','slug','has_trainees','has_radio_report','created_at')
    prepopulated_fields = {'slug':('name',)}
