from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    # Public & Farmer Portal
    path('', views.landing_view, name='landing'),
    path('home/', views.user_home, name='home'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    
    # AI Recognition Module
    path('ai-lens/', views.ai_lens_view, name='ai_lens'),
    path('api/recognize/', views.api_recognize_breed, name='api_recognize'),
    
    # Management / System Admin (Unique path to avoid Django Admin conflict)
    path('management/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('management/analytics/', views.admin_analytics_view, name='admin_analytics'),
    # path('management/toggle-user/<int:user_id>/', views.toggle_user_status, name='toggle_user'),
    path('management/validate/<int:scan_id>/', views.dataset_validate, name='dataset_validate'),
    path('management/discard/<int:scan_id>/', views.dataset_discard, name='dataset_discard'),
    path(
        'management/dataset-review/',
        views.admin_dataset_review,
        name='admin_dataset_review'
    ),
    path('about/', views.about_page, name='about'),
]