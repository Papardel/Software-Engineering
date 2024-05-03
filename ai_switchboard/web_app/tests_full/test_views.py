from django.test import TestCase, Client
from django.urls import reverse
from ..models import *


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.gateway_url = reverse('gateway')
        self.index_url = reverse('index')
        self.login_required_url = reverse('login_required')

        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_gateway_GET(self):
        response = self.client.get(self.gateway_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gateway.html')

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_required_GET(self):
        response = self.client.get(self.login_required_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_required.html')
