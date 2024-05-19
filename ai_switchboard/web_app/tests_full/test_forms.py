from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import LoginForm, UserCreationForm, UserChangeForm


class LoginFormTests(TestCase):
    def test_login_form_validates_correctly(self):
        form_data = {'username': 'testuser', 'password': 'testpass'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_handles_missing_fields(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class UserCreationFormTests(TestCase):
    def test_user_creation_form_validates_correctly(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpass321',
            'password2': 'testpass321',
            'email': 'testuser@example.com'
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_handles_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpass321',
            'password2': 'wrongpass321',
            'email': 'testuser@example.com'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserChangeFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_change_form_validates_correctly(self):
        form_data = {
            'username': 'newtestuser',
            'email': 'newtestuser@example.com',
            'date_joined': self.user.date_joined
        }
        form = UserChangeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_change_form_updates(self):
        form_data = {
            'username': 'newtestuser',
            'email': 'newtestuser@example.com',
            'date_joined': self.user.date_joined
        }
        form = UserChangeForm(instance=self.user, data=form_data)

        # Test that username and email are actually updated
        updated_user = form.save(commit=False)
        self.assertEqual(updated_user.username, 'newtestuser')
        self.assertEqual(updated_user.email, 'newtestuser@example.com')
