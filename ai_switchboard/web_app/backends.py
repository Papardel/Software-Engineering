from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from .models import AuthTable

class AuthTableBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = AuthTable.objects.get(username=username)
            if user.check_password(password):
                return user
        except AuthTable.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            return AuthTable.objects.filter(username=username).order_by('id').first()

    def get_user(self, user_id):
        try:
            return AuthTable.objects.get(pk=user_id)
        except AuthTable.DoesNotExist:
            return None