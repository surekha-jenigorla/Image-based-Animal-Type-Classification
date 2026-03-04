from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    filter_type = request.GET.get('filter', 'all')

    # Base queryset (used for counts)
    all_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Filtered queryset (used for display)
    notifications = all_notifications
    if filter_type == 'unread':
        notifications = notifications.filter(is_read=False)

    context = {
        'notifications': notifications,
        'unread_count': all_notifications.filter(is_read=False).count(),
        'filter_type': filter_type,
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required
def mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notification_list')


@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    return redirect('notifications:notification_list')
