from django.contrib import admin
from  .models import AttendanceRecord, AttendanceSession

# Register your models here.

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('session_label', 'instructor','department', 'created_at', 'expires_at')
    list_filter = ('department',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('trainee_name', 'trainee_phone', 'session', 'check_in', 'is_confirmed')
    list_filter = ('is_confirmed',)