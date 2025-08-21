# notifications/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from accounts.models import CustomUser
from posts.models import Post, Comment

# Helper to create notifications (This is perfect and should be kept as is)
def create_notification(recipient, actor, verb, target=None):
    target_content_type = None
    target_object_id = None
    if target:
        target_content_type = ContentType.objects.get_for_model(target)
        target_object_id = target.pk
    
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=target_content_type,
        target_object_id=target_object_id
    )


@login_required
def notification_list(request):
    """
    Displays the notifications for the current user.
    """
    # Filter for notifications for the logged-in user, showing unread first
    notifications = Notification.objects.filter(recipient=request.user).order_by('-read', '-timestamp')
    
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required
@require_POST
def mark_as_read(request, pk):
    """
    Marks a specific notification as read.
    """
    try:
        # Ensure only the recipient can mark their own notification as read
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notification.read = True
        notification.save()
        messages.success(request, "Notification marked as read.")
    except Notification.DoesNotExist:
        messages.error(request, "Notification not found or you don't have permission.")
    
    # Redirect back to the page the user came from, or to the notification list
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', redirect('notifications:notification-list')))