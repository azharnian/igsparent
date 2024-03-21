from django.contrib import admin
from .models import ReportStatus, ReportType, Report

# Register your models here.
admin.site.register(ReportStatus)
admin.site.register(ReportType)
admin.site.register(Report)