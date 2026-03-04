from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('mark-read/<int:pk>/', views.mark_read, name='mark_read'),
    path('delete/<int:pk>/', views.delete_notification, name='delete_notification'),
]