from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .forms import ReportRegisterForm, ReportFilterForm, ReportUpdateForm
from .models import Report
from users.models import Parent, Student
from users.decorators import parent_or_teacher_or_frontoffice_required, frontoffice_required, teacher_or_frontoffice_required, is_teacher, is_parent, is_frontoffice

# Create your views here.
@login_required
@parent_or_teacher_or_frontoffice_required
def home(request):
    student_reports = []
    if (is_frontoffice(request.user)):
        reports = Report.objects.filter(is_approved=False).all().order_by('-date_created')
        student_reports.extend(reports)

    if (is_parent(request.user)):
        parents = Parent.objects.filter(user=request.user).all()
        children = [parent.child.user for parent in parents]
        for child in children:
            student = Student.objects.filter(user=child).first()
            if student:
                reports = Report.objects.filter(student=student, is_approved=True).all().order_by('-date_created')
                student_reports.extend(reports)
    
    if (is_teacher(request.user)):
        reports = Report.objects.filter(created_by=request.user).all().order_by('-date_created')
        student_reports.extend(reports)

    # Paginate the reports
    paginator = Paginator(student_reports, 3)  # 10 reports per page
    page = request.GET.get('page')
    
    try:
        paginated_reports = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        paginated_reports = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results.
        paginated_reports = paginator.page(paginator.num_pages)

    return render(request, 'reports/home.html', {'student_reports' : paginated_reports})

@login_required
@teacher_or_frontoffice_required
def create_report(request):
    if request.method == 'POST':
        form = ReportRegisterForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            if is_teacher(request.user):
                report.is_approve = False
            report.save()
            messages.success(request, f'Your report has been created')
            return redirect('reports-home')
    form = ReportRegisterForm()
    return render(request, 'reports/create_report.html', {'form' : form})

@login_required
@frontoffice_required
def update_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        form = ReportUpdateForm(request.POST, instance=report)
        if form.is_valid():
            report.approved_by = request.user
            report.save()
            messages.success(request, f'Your report has been updated and approved')
            return redirect('reports-home')
    form = ReportUpdateForm(instance=report)
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