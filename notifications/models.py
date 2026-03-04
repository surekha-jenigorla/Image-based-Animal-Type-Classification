from django.db import models
from django.conf import settings

class Notification(models.Model):
    # Mapping to different icons observed in Figma: Complete, Maintenance, Feature, etc.
    TYPE_CHOICES = (
        ('success', 'Recognition Complete'),
        ('info', 'System Update'),
        ('warning', 'Maintenance'),
        ('feature', 'New Feature'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.user.email}"