from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.test_username = 'testuser'
        self.test_password = 'testpassword'
        User.objects.create_user(self.test_username, 'testuser@example.com', self.test_password)

    def test_login_success(self):
        response = self.client.post(self.login_url, {'username': self.test_username, 'password': self.test_password},follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)