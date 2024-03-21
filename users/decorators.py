from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from .models import Parent, FrontOffice

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def admin_required(view_func):
    # decorated_view_func = user_passes_test(is_admin)
    # return decorated_view_func(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_admin(request.user):
            return redirect('reports-home')  # Redirect to home page if not an admin
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def is_frontoffice(user):
    return FrontOffice.objects.filter(user=user).first()

def frontoffice_required(view_func):
    # decorated_view_func = user_passes_test(is_frontoffice)
    # return decorated_view_func(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_frontoffice(request.user):
            return redirect('reports-home')  # Redirect to home page if not an admin
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def is_parent(user):
    return Parent.objects.filter(user=user).first()

def parent_required(view_func):
    # decorated_view_func = user_passes_test(is_parent)
    # return decorated_view_func(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_parent(request.user):
            return redirect('reports-home')  # Redirect to home page if not an admin
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def parent_or_frontoffice_required(view_func):
    # decorated_view_func = user_passes_test(is_parent)
    # return decorated_view_func(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_frontoffice(request.user) and not is_parent(request.user):
            return redirect('reports-home')  # Redirect to home page if not an admin
        return view_func(request, *args, **kwargs)
    return _wrapped_view