from django.urls import reverse, resolve
from django.test import TestCase
from ..views import *


# Testing if the URLs resolve to the correct views
class TestURLs(TestCase):
    def test_home_url_resolves(self):
        url = reverse('gateway')
        self.assertEqual(resolve(url).func, gateway)

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, landing_page)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, user_login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, user_logout)

    def test_login_required_url_resolves(self):
        url = reverse('login_required')
        self.assertEqual(resolve(url).func, login_required_view)

    def test_upload_file_url_resolves(self):
        url = reverse('upload_file')
        self.assertEqual(resolve(url).func, upload_file)

    def test_media_url_resolves(self):
        url = reverse('media')
        self.assertEqual(resolve(url).func, media)

    def test_delete_file_url_resolves(self):
        url = reverse('delete_file', args=[1, 'file_type'])
        self.assertEqual(resolve(url).func, delete_file)

    def test_delete_all_files_url_resolves(self):
        url = reverse('delete_all_files')
        self.assertEqual(resolve(url).func, delete_all_files)

    def test_download_file_url_resolves(self):
        url = reverse('download_file', args=[1, 'file_type'])
        self.assertEqual(resolve(url).func, download_file)

    def test_process_video_url_resolves(self):
        url = reverse('process')
        self.assertEqual(resolve(url).func, process_view)

    def test_live_feed_url_resolves(self):
        url = reverse('live_feed')
        self.assertEqual(resolve(url).func, show_live_stream)

    def test_notifications_url_resolves(self):
        url = reverse('notifications')
        self.assertEqual(resolve(url).func, emergency_notifications)

    def test_latest_notification_url_resolves(self):
        url = reverse('latest_notification')
        self.assertEqual(resolve(url).func, latest_notification)
