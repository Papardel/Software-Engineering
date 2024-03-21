from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, login, logout, get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponse
import logging
from .forms import LoginForm, AuthTableCreationForm, AuthTablePasswordChangeForm
from .models import AuthTable
from django.shortcuts import render, redirect
from .forms import AuthTableCreationForm
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'index.html', {'user': request.user})


# Create your views here.
# Home page
def index(request):
    return render(request, 'index.html')


# login page
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = AuthTable.objects.get(username=username)
            if user.password == password:
                # User is authenticated successfully
                return HttpResponse("User authenticated successfully")
            else:
                # Password does not match
                return HttpResponse("Password does not match")
        except AuthTable.DoesNotExist:
            # User does not exist
            return HttpResponse("User does not exist")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


# When creating a new user
# When creating a new user

def create_user(request):
    if request.method == 'POST':
        form = AuthTableCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = AuthTableCreationForm()
    return render(request, 'create_user.html', {'form': form})


# When updating a user's password
def update_password(request):
    if request.method == 'POST':
        form = AuthTablePasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Add your logic here for what should happen after the password is changed
    else:
        form = AuthTablePasswordChangeForm(request.user)
    return render(request, 'update_password.html', {'form': form})
