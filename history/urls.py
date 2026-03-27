from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    # List all scans
    path('', views.history_list, name='history_list'),

    # View scan details
    path('<int:scan_id>/', views.history_detail, name='history_detail'),

    # Delete scan
    path('delete/<int:scan_id>/', views.history_delete, name='history_delete'),

    # Download report
    path('download/<int:id>/', views.download_report, name='download_report'),
]