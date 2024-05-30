from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import LoginForm, CameraFeedForm


class LoginFormTests(TestCase):
    def test_login_form_validates_correctly(self):
        form_data = {'username': 'testuser', 'password': 'testpass'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_handles_missing_fields(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
