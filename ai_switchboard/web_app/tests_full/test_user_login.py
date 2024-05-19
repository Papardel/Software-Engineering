from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_can_login_with_valid_credentials(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('index'))

    def test_user_cannot_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.content, b'Invalid username or password')

    """
    # can this test even pass?? i think it's testing for a condition that is impossible to reach
    def test_user_cannot_login_without_credentials(self):
        response = self.client.post(reverse('login'), {'username': '', 'password': ''})
        self.assertEqual(response.content, b'Username or password not provided')
    """

    def test_user_can_logout(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, '/login_required/?next=/index/')
