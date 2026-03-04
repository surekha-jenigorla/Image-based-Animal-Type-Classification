# profiles/context_processors.py
from recognition.models import BreedScan
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta

def profile_stats(request):
    if not request.user.is_authenticated:
        return {}

    scans = BreedScan.objects.filter(user=request.user)
    last_30_days = timezone.now() - timedelta(days=30)

    avg_acc = scans.aggregate(avg=Avg('confidence_score'))['avg'] or 0

    return {
        "drawer_total_scans": scans.count(),
        "drawer_avg_accuracy": f"{int(avg_acc)}%",
        "drawer_breeds": scans.values('breed_name').distinct().count(),
        "drawer_active_days": scans.filter(scanned_at__gte=last_30_days)
                                   .dates('scanned_at', 'day').count()
    }
