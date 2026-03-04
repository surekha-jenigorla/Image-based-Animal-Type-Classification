from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from recognition.models import BreedScan


# --------------------------------------------------
# Helper: derive health status from confidence score
# --------------------------------------------------
def get_health_status(confidence):
    if confidence >= 90:
        return "Excellent"
    elif confidence >= 75:
        return "Good"
    elif confidence >= 60:
        return "Moderate"
    return "Needs Review"


# --------------------------------------------------
# History List View
# --------------------------------------------------
@login_required
def history_list(request):
    filter_type = request.GET.get("filter")

    all_user_scans = (
        BreedScan.objects
        .filter(user=request.user)
        .order_by("-scanned_at")
    )

    # Apply filters
    scans = all_user_scans
    if filter_type == "high":
        scans = scans.filter(confidence_score__gte=90)
    elif filter_type == "low":
        scans = scans.filter(confidence_score__lt=70)

    context = {
        "scans": scans,
        "scan_count": all_user_scans.count(),
        "cattle_count": all_user_scans.filter(
            cattle_type__iexact="Cattle"
        ).count(),
        "buffalo_count": all_user_scans.filter(
            cattle_type__iexact="Buffalo"
        ).count(),
        "filter": filter_type,
    }

    return render(request, "history/history_list.html", context)


# --------------------------------------------------
# History Detail View
# --------------------------------------------------
@login_required
def history_detail(request, scan_id):
    scan = get_object_or_404(
        BreedScan,
        id=scan_id,
        user=request.user
    )

    context = {
        "scan": scan,
        "health_status": get_health_status(scan.confidence_score),
    }

    return render(request, "history/history_detail.html", context)


# --------------------------------------------------
# History Delete View
# --------------------------------------------------
@login_required
def history_delete(request, scan_id):
    scan = get_object_or_404(
        BreedScan,
        id=scan_id,
        user=request.user
    )

    if request.method == "POST":
        scan.delete()

    return redirect("history:history_list")
