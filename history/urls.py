from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    # List all scans for logged-in user
    path('', views.history_list, name='history_list'),

    # View single scan details
    path('<int:scan_id>/', views.history_detail, name='history_detail'),

    # Delete a scan
    path('delete/<int:scan_id>/', views.history_delete, name='history_delete'),
]
