import json
import base64
import PIL.Image
from google import genai
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db import models
from recognition.models import BreedScan
from breeds.models import Breed
from notifications.models import Notification

# ============================================================
# AI CONFIGURATION
# ============================================================
client = genai.Client(api_key=settings.AI_API_KEY)

# ============================================================
# PUBLIC VIEWS
# ============================================================

def landing_view(request):
    return render(request, 'landing.html')

# ============================================================
# USER PORTAL
# ============================================================

@login_required
def user_dashboard(request):
    user = request.user
    today = timezone.now().date()
    user_scans = BreedScan.objects.filter(user=user)

    total_scans = user_scans.count()

    # =========================================================
    # WEEKLY ACTIVITY (LAST 7 DAYS)
    # =========================================================
    start_week = today - timedelta(days=6)

    week_data = (
        user_scans
        .filter(scanned_at__date__range=[start_week, today])
        .extra(select={'day': "date(scanned_at)"})
        .values('day')
        .annotate(total=Count('id'))
    )

    week_map = {str(item['day']): item['total'] for item in week_data}
    max_w = max(week_map.values(), default=1) or 1

    weekly_activity = []
    for i in range(7):
        day = start_week + timedelta(days=i)
        val = week_map.get(str(day), 0)
        weekly_activity.append((
            day.strftime('%a'),
            val,
            int((val / max_w) * 100)
        ))

    # =========================================================
    # MONTHLY ACTIVITY (LAST 4 WEEKS)
    # =========================================================
    monthly_raw = []
    for i in range(3, -1, -1):
        w_start = today - timedelta(days=(i + 1) * 7)
        w_end = today - timedelta(days=i * 7)
        count = user_scans.filter(
            scanned_at__date__gt=w_start,
            scanned_at__date__lte=w_end
        ).count()
        monthly_raw.append((f"Week {4 - i}", count))

    max_m = max([x[1] for x in monthly_raw], default=1) or 1
    monthly_activity = [(l, v, int((v / max_m) * 100)) for l, v in monthly_raw]

    # =========================================================
    # YEARLY ACTIVITY (LAST 12 MONTHS)
    # =========================================================
    yearly_raw = []
    for i in range(11, -1, -1):
        m_date = today.replace(day=1) - timedelta(days=i * 30)
        count = user_scans.filter(
            scanned_at__year=m_date.year,
            scanned_at__month=m_date.month
        ).count()
        yearly_raw.append((m_date.strftime('%b'), count))

    max_y = max([x[1] for x in yearly_raw], default=1) or 1
    yearly_activity = [(l, v, int((v / max_y) * 100)) for l, v in yearly_raw]

    # =========================================================
    # TOP BREEDS
    # =========================================================
    top_breeds = (
        user_scans
        .values('breed_name', 'cattle_type')
        .annotate(count=Count('id'))
        .order_by('-count')[:3]
    )

    # =========================================================
    # METRICS
    # =========================================================
    unique_breeds = user_scans.values('breed_name').distinct().count()
    total_breeds = Breed.objects.filter(is_active=True).count()

    avg_confidence = round(
        user_scans.aggregate(avg=models.Avg('confidence_score'))['avg'] or 0,
        1
    )

    high_confidence = user_scans.filter(confidence_score__gte=90).count()
    success_rate = round((high_confidence / total_scans) * 100, 1) if total_scans else 0

    cattle_count = user_scans.filter(cattle_type='Cattle').count()
    buffalo_count = user_scans.filter(cattle_type='Buffalo').count()
    total_types = cattle_count + buffalo_count or 1
    # =========================================================
    # CURRENT MONTH SUMMARY
    # =========================================================
    current_month = today.month
    current_year = today.year

    month_scans = user_scans.filter(
        scanned_at__year=current_year,
        scanned_at__month=current_month
    )

    month_total_scans = month_scans.count()

    month_new_breeds = month_scans.values('breed_name').distinct().count()

    month_avg_confidence = round(
        month_scans.aggregate(avg=models.Avg('confidence_score'))['avg'] or 0,
        1
    )

    month_active_days = (
        month_scans
        .extra(select={'day': "date(scanned_at)"})
        .values('day')
        .distinct()
        .count()
    )

    context = {
        'total_scans': total_scans,
        'accuracy': int(avg_confidence),
        'unique_breeds': unique_breeds,
        'total_breeds': total_breeds,
        'avg_confidence': avg_confidence,
        'success_rate': success_rate,

        'weekly_activity': weekly_activity,
        'monthly_activity': monthly_activity,
        'yearly_activity': yearly_activity,

        'top_breeds': top_breeds,

        'cattle_count': cattle_count,
        'buffalo_count': buffalo_count,
        'cattle_pct': int((cattle_count / total_types) * 100),
        'buffalo_pct': int((buffalo_count / total_types) * 100),
        'month_name': today.strftime('%B'),
        'month_total_scans': month_total_scans,
        'month_new_breeds': month_new_breeds,
        'month_avg_confidence': month_avg_confidence,
        'month_active_days': month_active_days,
    }

    return render(request, 'portal/user_dashboard.html', context)

# ============================================================
# AI RECOGNITION
# ============================================================

@login_required
def ai_lens_view(request):
    return render(request, 'recognition/upload.html')


@login_required
def api_recognize_breed(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            image_content = PIL.Image.open(image_file)

            prompt = (
                "Identify the Indian cattle or buffalo breed in this image. "
                "Return ONLY JSON like: "
                "{\"breed\": \"name\", \"type\": \"type\", \"confidence\": 90}"
            )

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[prompt, image_content]
            )

            ai_data = json.loads(response.text.strip())

            scan_record = BreedScan.objects.create(
                user=request.user,
                image=image_file,
                breed_name=ai_data.get('breed'),
                cattle_type=ai_data.get('type'),
                confidence_score=ai_data.get('confidence'),
                is_validated=False  # dataset review flag
            )

            return JsonResponse({
                'status': 'success',
                'breed': scan_record.breed_name,
                'confidence': scan_record.confidence_score,
                'scan_id': scan_record.id
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# ============================================================
# ADMIN PANEL
# ============================================================

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard_view(request):
    return render(request, 'dashboards/admin_dashboard.html', {
        'total_users': get_user_model().objects.count(),
        'total_scans_global': BreedScan.objects.count(),
        'total_breeds_db': Breed.objects.count(),
        'system_status': 'Operational',
        'model_version': 'v2.1.4',
        'breeds_list': Breed.objects.all()[:10],
        'recent_global_scans': BreedScan.objects.all().order_by('-scanned_at')[:8]
    })


@user_passes_test(lambda u: u.is_superuser)
def admin_analytics_view(request):
    breed_counts = BreedScan.objects.values('breed_name').annotate(total=Count('id'))

    recent_uploads = BreedScan.objects.filter(
        is_validated=False
    ).order_by('-scanned_at')[:10]

    return render(request, 'dashboards/analytics.html', {
        'labels': [b['breed_name'] for b in breed_counts],
        'data': [b['total'] for b in breed_counts],
        'recent_uploads': recent_uploads,
        'total_training_images': BreedScan.objects.count(),
        'validated_count': BreedScan.objects.filter(is_validated=True).count(),
        'pending_count': BreedScan.objects.filter(is_validated=False).count(),
    })


@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if not user.is_superuser:
        user.is_active = not user.is_active
        user.save()
        messages.info(request, f"Status updated for {user.email}")
    return redirect('admin_user_directory')


# ============================================================
# DATASET VALIDATION
# ============================================================

@user_passes_test(lambda u: u.is_superuser)
def dataset_validate(request, scan_id):
    scan = get_object_or_404(BreedScan, id=scan_id)
    scan.is_validated = True
    scan.save()
    messages.success(request, "Image validated.")
    return redirect('portal:admin_analytics')


@user_passes_test(lambda u: u.is_superuser)
def dataset_discard(request, scan_id):
    scan = get_object_or_404(BreedScan, id=scan_id)
    scan.delete()
    messages.warning(request, "Image discarded.")
    return redirect('portal:admin_analytics')

def about_page(request):
    """View function for the About page"""
    return render(request, 'portal/about.html')

@login_required
def user_home(request):
    """
    Authenticated user Home page
    """
    return render(request, 'portal/home.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_dataset_review(request):
    pending_scans = (
        BreedScan.objects
        .filter(is_validated=False)
        .order_by('-scanned_at')
    )

    context = {
        'pending_scans': pending_scans,
        'pending_count': pending_scans.count(),
        'validated_count': BreedScan.objects.filter(is_validated=True).count(),
        'total_scans': BreedScan.objects.count(),
    }

    return render(request, 'dashboards/dataset_review.html', context)
