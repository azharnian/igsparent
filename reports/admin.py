from django.contrib import admin
from .models import ReportStatus, ReportType, Report

class ReportStatusAdmin(admin.ModelAdmin):
    list_display = (
        'report_status_title',
        'date_created'
    )

class ReportTypeAdmin(admin.ModelAdmin):
    list_display = (
        'report_type_title',
        'date_created'
    )

class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'date_created',
        'student',
        'report_title',
        'report_status',
        'is_approved',
        'created_by'
    )

    ordering = ('date_created',)

# Register your models here.
admin.site.register(ReportStatus, ReportStatusAdmin)
admin.site.register(ReportType, ReportTypeAdmin)
admin.site.register(Report, ReportAdmin)