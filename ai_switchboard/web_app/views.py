from django.contrib.auth import authenticate, login as auth_login, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from .forms import LoginForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import LoginForm  # make sure to import your login form
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)


@login_required
def landing_page(request):
    return render(request, 'index.html')


def login_required_view(request):
    return render(request, 'login_required.html')


# Index view. Renders the 'gateway.html' template.
def gateway(request):
    return render(request, 'gateway.html')


# Login view. If the request method is POST, it tries to authenticate the user.
# If the user is authenticated, it returns a success message.
# If the user is not authenticated, it returns an error message.
# If the request method is not POST, it renders the 'login.html' template with a LoginForm instance.
def user_login(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return HttpResponse("Invalid username or password")
        else:
            return HttpResponse("Username or password not provided")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')
