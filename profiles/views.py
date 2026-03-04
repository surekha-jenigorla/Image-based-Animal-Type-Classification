from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from recognition.models import BreedScan
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Dynamic calculations
    user_scans = BreedScan.objects.filter(user=request.user)
    total_scans = user_scans.count()
    
    # Calculate average accuracy
    avg_acc_val = user_scans.aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0
    
    # Date for "This Week" filter
    last_week = timezone.now() - timedelta(days=7)
    active_days = (
        user_scans
        .dates('scanned_at', 'day')
        .count()
    )
    
    context = {
        'profile': profile,
        'total_scans': total_scans,
        'this_week': user_scans.filter(scanned_at__gte=last_week).count(),
        'breeds_found': user_scans.values('breed_name').distinct().count(),
        # Fixed: Ensuring int conversion for the UI percentage display
        'avg_accuracy': f"{int(avg_acc_val)}%" if total_scans else "0%",
        'joined_on': request.user.date_joined.strftime("%B %Y"),
        'days_active': active_days,
    }
    return render(request, 'profiles/profile_view.html', context)


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Direct assignment from POST data
        profile.full_name = request.POST.get('full_name')
        profile.phone_number = request.POST.get('phone_number')
        profile.farm_location = request.POST.get('farm_location')
        profile.bio = request.POST.get('bio')
        
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')
            
        profile.save()
        return redirect('profiles:profile_view')
        
    return render(request, 'profiles/profile_edit.html', {'profile': profile})