from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ReportRegisterForm, ReportFilterForm
from .models import Report
from users.models import Parent, Student
from users.decorators import parent_or_frontoffice_required, frontoffice_required

# Create your views here.
@login_required
@parent_or_frontoffice_required
def home(request):
    parents = Parent.objects.filter(user=request.user).all()
    children = [parent.child.user for parent in parents]
    student_reports = []
    for child in children:
        student = Student.objects.filter(user=child).first()
        if student:
            reports = Report.objects.filter(student=student).all()
            student_reports.extend(reports)

    return render(request, 'reports/home.html', {'student_reports' : student_reports})

@login_required
@frontoffice_required
def create_report(request):
    if request.method == 'POST':
        form = ReportRegisterForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user

            report.save()
            messages.success(request, f'Your report has been created')
    form = ReportRegisterForm()
    return render(request, 'reports/create_report.html', {'form' : form})

@login_required
@frontoffice_required
def view_reports(request):
    reports = []
    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            reports = form.filter_reports()

    form = ReportFilterForm()
    context = {
        'reports' : reports,
        'form' : form
    }
    return render(request, 'reports/view_reports.html', context)