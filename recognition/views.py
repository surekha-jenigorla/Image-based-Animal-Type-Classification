import time
import logging
import PIL.Image

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import BreedScan
from notifications.models import Notification
from .gemini_service import analyze_with_gemini


logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def upload_image(request):

    if request.method == "POST" and request.FILES.get("image"):

        image_file = request.FILES["image"]

        try:
            img = PIL.Image.open(image_file).convert("RGB")
            image_file.seek(0)
        except Exception:
            return render(request, "recognition/upload.html", {
                "error": "Invalid image file."
            })

        start_time = time.time()

        ai_data = None
        ai_source = "gemini"

        # PRIMARY AI — GEMINI
        try:
            logger.info("Attempting Gemini recognition...")
            ai_data = analyze_with_gemini(img)

        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            ai_data = None

        # Final Safe Fallback
        if not ai_data:
            ai_data = {
                "breed": "Unknown",
                "type": "Cattle",
                "confidence": 0
            }
            ai_source = "fallback"

        processing_time = int((time.time() - start_time) * 1000)

        scan = BreedScan.objects.create(
            user=request.user,
            image=image_file,
            breed_name=ai_data.get("breed", "Unknown"),
            cattle_type=ai_data.get("type", "Cattle"),
            confidence_score=ai_data.get("confidence", 0),
            processing_time_ms=processing_time,
            ai_source=ai_source
        )

        Notification.objects.create(
            user=request.user,
            title="Recognition Complete",
            message=f"{scan.breed_name} detected with {scan.confidence_score}%",
            notification_type="success"
        )

        return render(request, "recognition/result.html", {
            "result": scan
        })

    return render(request, "recognition/upload.html")
