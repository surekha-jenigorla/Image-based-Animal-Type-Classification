from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    farm_location = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/avatars/', default='profiles/default_avatar.png')
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Profile for {self.user.email}"