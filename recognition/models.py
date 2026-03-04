from django.db import models
from django.conf import settings


class BreedScan(models.Model):
    CATTLE_TYPES = (
        ('Cattle', 'Cattle'),
        ('Buffalo', 'Buffalo'),
    )

    AI_SOURCES = (
        ('gemini', 'Gemini'),
        ('local', 'Local Model'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scans'
    )

    breed = models.ForeignKey(
        'breeds.Breed',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='scans'
    )

    image = models.ImageField(upload_to='scans/%Y/%m/%d/')
    breed_name = models.CharField(max_length=100)
    cattle_type = models.CharField(max_length=10, choices=CATTLE_TYPES)
    confidence_score = models.FloatField()
    ai_source = models.CharField(max_length=20, choices=AI_SOURCES, default='gemini')
    processing_time_ms = models.PositiveIntegerField(null=True, blank=True)
    scanned_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.breed_name} - {self.user.email}"


class DatasetImage(models.Model):
    breed = models.ForeignKey('breeds.Breed', on_delete=models.CASCADE, related_name='dataset_images')
    image = models.ImageField(upload_to='dataset/training/')
    is_validated = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Training Image for {self.breed.name}"
