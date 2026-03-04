from .models import Notification

def notification_count(request):
    """
    Provides unread notification count globally
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return {"notification_count": count}
    return {"notification_count": 0}
