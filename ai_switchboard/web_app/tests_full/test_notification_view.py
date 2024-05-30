from django.test import TestCase, RequestFactory
from django.urls import reverse
from ..models import Notification
from ..views import emergency_notifications, get_latest_notification
from django.contrib.auth.models import User
import threading
import time
import json


class EmergencyNotificationsTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_emergency_notifications(self):

        Notification.objects.create(message='Emergency notification 1', is_emergency=True, user=self.user)
        Notification.objects.create(message='Emergency notification 2', is_emergency=True, user=self.user)

        request = self.factory.get(reverse('notifications'))
        response = emergency_notifications(request)

        self.assertContains(response, 'Emergency notification 1')
        self.assertContains(response, 'Emergency notification 2')


class GetLatestNotificationTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_get_latest_notification(self):

        notification = Notification.objects.create(message='Emergency notification', is_emergency=True, user=self.user)

        request = self.factory.get(reverse('latest_notification'))
        response = get_latest_notification(request)

        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Emergency notification')
        self.assertEqual(data['time_of_save'], notification.time_of_save.isoformat())
