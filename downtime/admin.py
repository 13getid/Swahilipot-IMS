from django.contrib import admin
from .models import DowntimeReport
# Register your models here.

@admin.register(DowntimeReport)
class DowntimeReportAdmin(admin.ModelAdmin):
    list_display = ('frequency_band', 'severity', 'status', 'instructor', 'reported_at')
    list_filter = ('status', 'severity')