from django.contrib import admin
from .models import FormSubmission
# Register your models here.

@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'form_type', 'instructor', 'department', 'status','submitted_at')
    list_filter = ('status', 'department')
