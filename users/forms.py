from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .decorators import is_parent, is_frontoffice, is_admin, is_teacher
from .models import Profile, Parent, Student


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=32)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # Profile.objects.create(user=user, phone=self.cleaned_data['phone'])
            profile = Profile.objects.get(user_id=user.id)
            profile.phone = self.cleaned_data['phone']
            profile.save()

        return user

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )
        
        if not is_admin(user) and not is_frontoffice(user) and not is_parent(user) and not is_teacher(user):
            raise forms.ValidationError(
                ("Your account is not available."),
                code='unavailable',
            )

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name' ,'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone']

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

class ParentRegisterForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['user', 'child', 'relation']

class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['cohort_name', 'user']

class UserFilterForm(forms.Form):
    TYPE_CHOICES = [
        ('Parent', 'Parent'),
        ('Student', 'Student'),
    ]

    name = forms.CharField(max_length=100, required=False)
    user_type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)
    
    def filter_users(self):
        name = self.cleaned_data.get('query_text')
        user_type = self.cleaned_data.get('user_type')

        if user_type:
            if user_type == 'Parent':
                parents = Parent.objects.all()
                users = [parent.user for parent in parents]
            elif user_type == 'Student':
                students = Student.objects.all()
                users = [student.user for student in students]
        # else:
        #     users = list(User.objects.filter(is_staff=False, is_superuser=False).all())

        user_ids = set([user.id for user in users])
        users = User.objects.filter(id__in=user_ids)

        if name:
            users = users.filter(first_name__icontains=name)

        return users