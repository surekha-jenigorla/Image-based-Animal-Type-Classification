from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP
import random

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_active:
                messages.error(request, 'Please verify your email first.')
                return render(request, 'accounts/login.html')

            login(request, user)
            user.login_count += 1
            user.save()
            
            # Role-based redirection logic
            if user.role == 'admin' or user.is_superuser:
                return redirect('portal:admin_dashboard') # To adminpanel app
            return redirect('portal:user_dashboard') # To portal app
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'farmer') # Capture role from form

        if User.objects.filter(email=email).exists():
            messages.info(request, 'User already exists. Please login.')
            return redirect('login')

        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            is_active=False
        )

        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})

        try:
            send_mail(
                'Verify your Cattle Breed Recognition Account',
                f'Your OTP code is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Mail error: {e}") # Standard academic logging

        request.session['verify_user'] = user.id
        return redirect('verify_otp')

    return render(request, 'accounts/signup.html')

def verify_otp_view(request):
    user_id = request.session.get('verify_user')
    if not user_id:
        return redirect('signup')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=user).first()

        if otp_obj and not otp_obj.is_expired() and entered_otp == otp_obj.otp:
            user.is_active = True
            user.is_verified = True
            user.save()
            otp_obj.delete()
            del request.session['verify_user']
            return render(request, 'accounts/verify_success.html')

        messages.error(request, 'Invalid or expired OTP.')

    return render(request, 'accounts/verify_otp.html')

def logout_view(request):
    logout(request)
    return redirect('landing')