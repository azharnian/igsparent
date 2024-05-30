from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='reports-home'),
    path('create/', views.create_report, name='reports-create'),
    path('view/', views.view_reports, name='reports-view'),
    path('update/<str:report_id>', views.update_report, name='reports-update' ),
]