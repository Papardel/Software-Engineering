from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import AuthTable


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AuthTableCreationForm(UserCreationForm):
    class Meta:
        model = AuthTable
        fields = ('username', 'password')


class AuthTablePasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = AuthTable
        fields = ('username', 'password')
