from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

User = get_user_model()

# Custom authentication backend
class UserBackend(ModelBackend):
    # Called when a user tries to log in
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to get the user from the User model
            user = User.objects.get(username=username)
            # If the user exists, check if the provided password is correct
            if user.check_password(password):
                # If the password is correct, return the user
                return user
        except User.DoesNotExist:
            # If the user does not exist, do nothing and pass
            pass
        except MultipleObjectsReturned:
            # If multiple users with the same username exist, return the first one
            return User.objects.filter(username=username).order_by('id').first()

    # This method is called to get a User object from a user ID
    def get_user(self, user_id):
        try:
            # Try to get the user from the User model
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # If the user does not exist, return None
            return None