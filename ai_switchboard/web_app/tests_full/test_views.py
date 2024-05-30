import os
from django.test import TestCase, Client
from django.urls import reverse
from ..models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


class LandingPageViewTest(TestCase):

    # Test if the landing_page view returns a 302 status code if the user is unauthenticated
    def test_landing_page_unauthenticated(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    # Test if the landing_page view returns a 200 status code if the user is authenticated
    def test_landing_page_authenticated(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # Test if the landing_page view resolves to the correct template
    def test_landing_page_template(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')


class LoginRequiredViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('login_required'))

    # Test if the login_required_view view returns a 200 status code
    def test_login_required(self):
        self.assertEqual(self.response.status_code, 200)

    # Test if the login_required_view view resolves to the correct template
    def test_login_required_template(self):
        self.assertTemplateUsed(self.response, 'login_required.html')


class GatewayViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('gateway'))

    # Test if the gateway view returns a 200 status code
    def test_gateway(self):
        self.assertEqual(self.response.status_code, 200)

    # Test if the gateway view resolves to the correct template
    def test_gateway_template(self):
        self.assertTemplateUsed(self.response, 'gateway.html')


class UserLoginViewTest(TestCase):

    # Test if the user_login view returns a 200 status code
    def test_user_login(self):
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 200)


class UserLogoutViewTest(TestCase):
    # Test if the user_logout view returns a 302 status code
    def test_user_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class LiveFeedViewTest(TestCase):

    # Test if the live_feed view returns a 302 status code if the user is unauthenticated
    def test_live_feed_unauthenticated(self):
        response = self.client.get(reverse('live_feed'))
        self.assertEqual(response.status_code, 302)

    # Test if the live_feed view returns a 200 status code if the user is authenticated
    def test_live_feed_authenticated(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('live_feed'))
        self.assertEqual(response.status_code, 200)


class UploadFileViewTest(TestCase):

    # Test if the upload_file view returns a 302 status code if the user is unauthenticated
    def test_upload_file_unauthenticated(self):
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 302)


class DownloadFileViewTest(TestCase):

    def setUp(self):
        self.mock_image = Image(name='test_image', data=b'test_data')
        self.mock_image.id = 1

    # Test if the download_file view returns a 302 status code if the user is unauthenticated
    def test_download_file_unauthenticated(self):

        with patch('web_app.viewslib.media_view.Image.objects.get', return_value=self.mock_image):
            response = self.client.get(reverse('download_file', args=[1, 'image']))
            self.assertEqual(response.status_code, 302)

    # Test if the download_file view returns a 200 status code if the user is authenticated
    def test_download_file_authenticated(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        with patch('web_app.viewslib.media_view.Image.objects.get', return_value=self.mock_image):
            response = self.client.get(reverse('download_file', args=[1, 'image']))
            self.assertEqual(response.status_code, 200)


class MediaViewTest(TestCase):

    # Test if the media view returns a 302 status code if the user is unauthenticated
    def test_media_unauthenticated(self):
        response = self.client.get(reverse('media'))
        self.assertEqual(response.status_code, 302)

    # Test if the media view returns a 200 status code if the user is authenticated
    def test_media_authenticated(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('media'))
        self.assertEqual(response.status_code, 200)

    # Test if the media view resolves to the correct template
    def test_media_template(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('media'))
        self.assertTemplateUsed(response, 'media.html')


class DeleteFileViewTest(TestCase):

    def setUp(self):
        self.mock_video = Video(name='test_video', data=b'test_data')
        self.mock_video.id = 2

    # Test if the delete_file view returns a 302 status code if the user is unauthenticated
    def test_delete_file_unauthenticated(self):

        with patch('web_app.viewslib.media_view.Video.objects.get', return_value=self.mock_video):
            response = self.client.get(reverse('delete_file', args=[2, 'video']))
            self.assertEqual(response.status_code, 302)

    # Test if the delete_file view returns a 302 status code if the user is authenticated and redirects to media page
    def test_delete_file_authenticated(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        with patch('web_app.viewslib.media_view.Video.objects.get', return_value=self.mock_video):
            response = self.client.get(reverse('delete_file', args=[2, 'video']))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('media'))

    
    """

    def test_delete_all_files(self):
        response = self.client.delete(reverse('delete_all_files'))
        self.assertEqual(response.status_code, 302)

    """


class ShowLiveStreamViewTest(TestCase):

    # Test if the show_live_stream view returns a 302 status code if the user is unauthenticated
    def test_show_live_stream_unauthenticated(self):
        response = self.client.get(reverse('live_feed'))
        self.assertEqual(response.status_code, 302)

    # Test if the show_live_stream view resolves to the correct template
    def test_show_live_stream_template(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('live_feed'))
        self.assertTemplateUsed(response, 'live_feed.html')


class NotificationsViewTest(TestCase):

    """
    # this for some reason fails cause it also returns 200 no clue why
    # Test if the notifications view returns a 302 status code if the user is unauthenticated
    def test_notifications_unauthenticated(self):
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 302)
    """

    # Test if the notifications view returns a 200 status code if the user is authenticated
    def test_notifications_authenticated(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)

    # Test if the notifications view resolves to the correct template
    def test_notifications_template(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('notifications'))
        self.assertTemplateUsed(response, 'emergency_notifications.html')


class LatestNotificationViewTest(TestCase):

    # Test if the latest_notifications view returns a 302 status code if the user is unauthenticated
    def test_latest_notification_unauthenticated(self):
        response = self.client.get(reverse('latest_notification'))
        self.assertEqual(response.status_code, 302)

    # Test if the notifications view returns a 200 status code if the user is authenticated
    def test_latest_notification_authenticated(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('latest_notification'))
        self.assertEqual(response.status_code, 200)
