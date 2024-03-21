from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register, name='users-register'),
    path('profile/', views.profile, name='users-profile'),
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='users/change_password.html'), name='users-password-change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),name='password_change_done'),
    path('parent-assign/', views.assign_parent, name='users-parent-assign'),
    path('student-assign/', views.assign_student, name='users-student-assign'),
    path('view/', views.view_users, name='users-view'),
]