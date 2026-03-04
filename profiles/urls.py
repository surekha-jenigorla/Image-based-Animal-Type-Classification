from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # Maps to domain.com/profile/me/
    path('me/', views.profile_view, name='profile_view'),
    # Maps to domain.com/profile/me/edit/
    path('me/edit/', views.profile_edit, name='profile_edit'),
]