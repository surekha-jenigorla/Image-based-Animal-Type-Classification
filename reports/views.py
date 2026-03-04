from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recognition.models import BreedScan
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


@login_required
def report_dashboard(request):
    scans = BreedScan.objects.filter(user=request.user)

    # Summary metrics
    total_scans = scans.count()
    breeds_count = scans.values('breed_name').distinct().count()

    # Pie chart: breed distribution
    breed_data = scans.values('breed_name').annotate(count=Count('id'))
    breed_labels = [item['breed_name'] for item in breed_data]
    breed_values = [item['count'] for item in breed_data]

    # Bar chart: monthly scans
    monthly_data = scans.annotate(month=TruncMonth('scanned_at')) \
                        .values('month') \
                        .annotate(count=Count('id')) \
                        .order_by('month')

    month_labels = [
        item['month'].strftime("%b %Y") if item['month'] else ""
        for item in monthly_data
    ]

    month_values = [item['count'] for item in monthly_data]

    context = {
        'total_scans': total_scans,
        'breeds_count': breeds_count,
        'breed_labels': json.dumps(breed_labels),
        'breed_values': json.dumps(breed_values),
        'month_labels': json.dumps(month_labels),
        'month_values': json.dumps(month_values),
    }

    return render(request, 'reports/report_dashboard.html', context)

@login_required
def download_report(request):
    scans = BreedScan.objects.filter(user=request.user)

    total_scans = scans.count()
    breeds_count = scans.values('breed_name').distinct().count()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="livestock_report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 60

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y, "Livestock Statistics Report")

    y -= 40
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Total Scans: {total_scans}")

    y -= 25
    p.drawString(50, y, f"Unique Breeds: {breeds_count}")

    y -= 40
    p.drawString(50, y, "Generated automatically by the system")

    p.showPage()
    p.save()

    return response