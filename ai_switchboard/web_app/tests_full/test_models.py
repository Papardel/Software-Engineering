from django.test import TestCase
from ..models import Image, Video, CSV, JSON, Text, Notification, Camera
from django.contrib.auth.models import User
from datetime import datetime


# Test that model creations produce the correct fields
class ImageModelTest(TestCase):
    def test_image_creation_produces_correct_fields(self):
        image = Image.objects.create(name='test_image', data=b'test_data')
        self.assertEqual(image.name, 'test_image')
        self.assertEqual(image.data, b'test_data')
        self.assertIsInstance(image.date_of_save, datetime)


class VideoModelTest(TestCase):
    def test_video_creation_produces_correct_fields(self):
        video = Video.objects.create(name='test_video', data=b'test_data')
        self.assertEqual(video.name, 'test_video')
        self.assertEqual(video.data, b'test_data')
        self.assertIsInstance(video.date_of_save, datetime)


class CSVModelTest(TestCase):
    def test_csv_creation_produces_correct_fields(self):
        csv = CSV.objects.create(name='test_csv', data='test_data')
        self.assertEqual(csv.name, 'test_csv')
        self.assertEqual(csv.data, 'test_data')
        self.assertIsInstance(csv.date_of_save, datetime)


class JSONModelTest(TestCase):
    def test_json_creation_produces_correct_fields(self):
        json = JSON.objects.create(name='test_json', data='test_data')
        self.assertEqual(json.name, 'test_json')
        self.assertEqual(json.data, 'test_data')
        self.assertIsInstance(json.date_of_save, datetime)


class TextModelTest(TestCase):
    def text_creation_produces_correct_fields(self):
        text = Text.objects.create(name='test_text', data='test_data')
        self.assertEqual(text.name, 'test_text')
        self.assertEqual(text.data, 'test_data')
        self.assertIsInstance(text.date_of_save, datetime)


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')

    def test_notification_creation_produces_correct_fields(self):
        notification = Notification.objects.create(message='test_message', user=self.user)
        self.assertEqual(notification.message, 'test_message')
        self.assertEqual(notification.user, self.user)
        self.assertIsInstance(notification.time_of_save, datetime)


class CameraModelTest(TestCase):
    def test_camera_creation_produces_correct_fields(self):
        camera = Camera.objects.create(name='test_camera')
        self.assertEqual(camera.name, 'test_camera')

    def test_camera_str_representation(self):
        camera = Camera.objects.create(name='Test Camera')
        self.assertEqual(str(camera), 'Test Camera')
