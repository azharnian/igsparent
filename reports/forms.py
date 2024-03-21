from django import forms
from users.models import User, Student
from .models import ReportType, ReportStatus ,Report

class ReportRegisterForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['student', 'report_type', 'report_title', 'report_content', 'image', 'report_status']

class ReportFilterForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all().order_by('user__first_name'), required=False, empty_label="All Students")
    report_type = forms.ModelChoiceField(queryset=ReportType.objects.all(), required=False, empty_label="All Report Types")
    report_status = forms.ModelChoiceField(queryset=ReportStatus.objects.all(), required=False, empty_label="All Report Statuses")

    def filter_reports(self):
        queryset = Report.objects.all()
        student = self.cleaned_data.get('student')
        report_type = self.cleaned_data.get('report_type')
        report_status = self.cleaned_data.get('report_status')

        if student:
            queryset = queryset.filter(student=student)
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        if report_status:
            queryset = queryset.filter(report_status=report_status)

        return queryset