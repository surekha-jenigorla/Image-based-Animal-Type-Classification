from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, signup_view, verify_otp_view

urlpatterns = [
    # Custom Authentication & OTP Flow (Verified in Batch 1 & 2 Extraction)
    path('login/', login_view, name='login'), 
    path('signup/', signup_view, name='signup'), 
    path('logout/', logout_view, name='logout'), 
    path('verify-otp/', verify_otp_view, name='verify_otp'),

    # Password Reset Logic (Required for B.Tech academic completeness)
    # This single line handles password_reset, password_reset_done, etc.
    # It will automatically look for the files in your 'templates/registration' folder
    path('', include('django.contrib.auth.urls')), 
]