import threading
import time
from django.shortcuts import render
from ai_switchboard.web_app.models import Notification


def emergency_notifications(request):
    notifications = Notification.objects.filter(is_emergency=True, is_read=False)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return render(request, 'emergency_notifications.html', {'notifications': notifications})


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


emergency_notification_thread = threading.Thread(target=emergency_notification_thread)
emergency_notification_thread.daemon = True
emergency_notification_thread.start()
