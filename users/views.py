import os
import csv

from django.conf import settings
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .models import Profile
from django.contrib.auth.models import User
from users.models import Parent, Student
from reports.models import Report
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeForm, ParentRegisterForm, StudentRegisterForm, UserFilterForm, CSVUsersUploadForm
from users.decorators import frontoffice_required, is_parent, is_student

@login_required
def home(request):
    return redirect('reports-home')

@login_required
@frontoffice_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account has been created!')
            return redirect('users-register')
    form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
@frontoffice_required
def upload_users(request):

    if request.method == 'POST':
        form = CSVUsersUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            try:
                decoded_file = csv_file.read().decode('utf-8')
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(decoded_file)
                decoded_file = decoded_file.splitlines()
                reader = csv.DictReader(decoded_file, dialect=dialect)
                
                for index, row in enumerate(reader, start=1):
                    try:
                        form = UserRegisterForm({
                            'username': row['username'],
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                            'email': row['email'],
                            'password1': row['password'],
                            'password2': row['password'],
                            'phone': row['phone']
                        })
                        if form.is_valid():
                            form.save()
                        else:
                            error_list = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
                            error_message = f"Error in row {index}: " + "; ".join(error_list)
                            messages.error(request, error_message)
                    except Exception as e:
                        messages.error(request, f"Error processing row {row}: {str(e)}")
                
                messages.success(request, 'Users have been uploaded successfully!')
                return redirect('users-upload')
            except csv.Error as e:
                messages.error(request, f"CSV file error: {str(e)}")
    else:
        form = CSVUsersUploadForm()

    return render(request, 'users/upload_users.html', {'form': form})

@login_required
@frontoffice_required
def assign_student(request):
    pass

@login_required
@frontoffice_required
def assign_parent(request):
    if request.method == 'POST':
        form = ParentRegisterForm(request.POST)
        if form.is_valid():
            parent = form.save(commit=False)
            parent.assigned_by = request.user
            
            parent.save()
            messages.success(request, f'Account has been assinged!')
        else:
            messages.warning(request, f'Failed assinged!')
    form = ParentRegisterForm()
    return render(request, 'users/parent_assign.html', {'form': form})

@login_required
@frontoffice_required
def assign_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.enrolled_by = request.user
            
            student.save()
            messages.success(request, f'Account has been assinged!')
        else:
            messages.warning(request, f'Failed assinged!')

    form = StudentRegisterForm()
    return render(request, 'users/student_assign.html', {'form': form})

@login_required
def profile(request):
    # if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST,
    #                                request.FILES,
    #                                instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Your account has been updated!')
    #         return redirect('users-profile')
    #     else:
    #         messages.warning(request, 'There was an error in the form. Please correct it.')

    # else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
@frontoffice_required
def edit(request, username):
    user = User.objects.filter(username=username).first()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'The account of {user.username} has been updated!')
            return redirect('users-view')
        else:
            messages.warning(request, 'There was an error in the form. Please correct it.')

    else:   
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'edit_user' : user
    }
    return render(request, 'users/edit_profile.html', context)

@login_required
@frontoffice_required
def detail(request, username):
    user = User.objects.filter(username=username).first()
    children, reports = [], []

    if(is_parent(user)):
        parents = Parent.objects.filter(user=user).all()
        children = [parent.child.user for parent in parents]
    elif (is_student(user)):
        student = Student.objects.filter(user=user).first()
        reports = Report.objects.filter(student=student).all().order_by('-date_created')

    context = {
        'detail_user' : user,
        'children' : children,
        'reports' : reports
    }

    print(children, reports, user)
    return render(request, 'users/detail_relation.html', context)

@login_required
def change_password(request):
    form = PasswordChangeForm()
    return render(request, 'users/change_password.html', {'form' : form})

@login_required
@frontoffice_required
def view_users(request):
    users = []
    if request.method == 'POST':
        form = UserFilterForm(request.POST)
        if form.is_valid():
            users = form.filter_users()

    form = UserFilterForm()
    context = {
        'users' : users,
        'form' : form
    }
    return render(request, 'users/view_users.html', context)

@login_required
@frontoffice_required
def download_sample_csv(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'csv', 'sample.csv')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="sample.csv"'
            return response
    else:
        return HttpResponse('File not found.', status=404)