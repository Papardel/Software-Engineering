import threading
import time

from django.http import JsonResponse
from django.shortcuts import render
from ..models import Notification


def emergency_notifications(request):
    emergency_notifications_list = Notification.objects.filter(is_emergency=1)
    return render(request, 'emergency_notifications.html', {'notifications': emergency_notifications_list})


def emergency_notification_thread():
    last_notification_id = None
    while True:
        # Get the latest emergency notification from the database
        latest_notification = Notification.objects.filter(is_emergency=True, is_read=False).order_by('-id').first()
        if latest_notification is not None and latest_notification.id != last_notification_id:
            # Set the is_read field of the notification to True
            latest_notification.is_read = True
            latest_notification.save()
            last_notification_id = latest_notification.id
        time.sleep(5)  # Wait for 5 seconds before checking for new notifications again


def get_latest_notification(request):
    latest = Notification.objects.filter(is_emergency=1, is_read=False).order_by('-time_of_save').first()
    if latest:
        latest.update(is_read=True)
        return JsonResponse({'message': latest.message, 'time_of_save': latest.time_of_save.isoformat()})
    else:
        return JsonResponse({'message': None})


emergency_notification_thread = threading.Thread(target=emergency_notification_thread)
emergency_notification_thread.daemon = True
emergency_notification_thread.start()
