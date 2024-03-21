from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import frontoffice_required, admin_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeForm, ParentRegisterForm, StudentRegisterForm, UserFilterForm

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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users-profile')
        else:
            messages.warning(request, 'There was an error in the form. Please correct it.')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render(request, 'users/profile.html', context)

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