from django.urls import path
from . import views

app_name = 'breeds'

urlpatterns = [
    # user
    path('', views.breed_list, name='breed_list'),
    path('<int:pk>/', views.user_breed_detail, name='breed_detail'),

    # admin
    path('admin/manage/', views.admin_breed_manage, name='admin_breed_manage'),
    path('admin/add/', views.add_breed, name='add_breed'),
    path('admin/edit/<int:pk>/', views.edit_breed, name='edit_breed'),
    path('admin/delete/<int:pk>/', views.delete_breed, name='delete_breed'),
    path('admin/<int:pk>/', views.admin_breed_detail, name='admin_breed_detail'),
]
