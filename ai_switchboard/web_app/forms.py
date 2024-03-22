from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import AuthTable


# LoginForm is a Django Form for user login. It has two fields: 'username' and 'password'.
class LoginForm(forms.Form):
    username = forms.CharField()  # The 'username' field is a CharField.
    password = forms.CharField(
        widget=forms.PasswordInput)  # The 'password' field is a CharField that uses a PasswordInput widget.


# AuthTableCreationForm is a Django Form for creating a new user. It inherits from Django's UserCreationForm.
class AuthTableCreationForm(UserCreationForm):
    class Meta:
        model = AuthTable  # Specifies that this form uses the AuthTable model.
        fields = ('username', 'password')  # Specifies that this form has two fields: 'username' and 'password'.


# AuthTablePasswordChangeForm is a Django Form for changing a user's password. It inherits from Django's
# PasswordChangeForm.
class AuthTablePasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = AuthTable  # Specifies that this form uses the AuthTable model.
        fields = ('username', 'password')  # Specifies that this form has two fields: 'username' and 'password'.
