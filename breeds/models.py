from django.db import models


class Breed(models.Model):
    CATEGORY_CHOICES = (
        ('Cattle', 'Cattle'),
        ('Buffalo', 'Buffalo'),
    )

    # =========================
    # BASIC INFO
    # =========================
    name = models.CharField(
        max_length=100,
        unique=True
    )

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='Cattle'
    )

    thumbnail = models.ImageField(
        upload_to='breeds/thumbnails/',
        blank=True,
        null=True,
        help_text="Optional thumbnail image for gallery and detail pages"
    )

    description = models.TextField()

    origin_location = models.CharField(
        max_length=150
    )

    # =========================
    # PRODUCTION METRICS
    # =========================
    milk_yield = models.CharField(
        max_length=50,
        help_text="e.g., 15–20 L/day"
    )

    milk_fat = models.CharField(
        max_length=20,
        blank=True,
        help_text="e.g., 4–6%"
    )

    daily_yield = models.CharField(
        max_length=50,
        blank=True,
        help_text="Alternative yield display (optional)"
    )

    # =========================
    # APPEARANCE & TRAITS
    # =========================
    color_description = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., Black & White, Brown, Fawn"
    )

    traits = models.TextField(
        blank=True,
        help_text="Comma separated traits, e.g. Heat tolerant, Disease resistant"
    )

    # =========================
    # OPTIONAL MEDIA
    # =========================
    video_link = models.URLField(
        blank=True,
        null=True,
        help_text="Optional YouTube or reference video link"
    )

    # =========================
    # SYSTEM FIELDS
    # =========================
    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Breed"
        verbose_name_plural = "Breeds"

    def __str__(self):
        return self.name

    # =========================
    # TEMPLATE HELPERS
    # =========================
    @property
    def thumbnail_url(self):
        """
        Safe thumbnail accessor for templates.
        """
        if self.thumbnail:
            return self.thumbnail.url
        return "https://via.placeholder.com/400"

    @property
    def traits_list(self):
        """
        Converts comma-separated traits into a list for templates.
        """
        if not self.traits:
            return []
        return [t.strip() for t in self.traits.split(',') if t.strip()]
