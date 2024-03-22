from django.contrib.auth import authenticate, login as auth_login, login, logout, get_user_model
from django.http import JsonResponse, HttpResponse
import logging
from .forms import LoginForm, AuthTableCreationForm, AuthTablePasswordChangeForm
from django.shortcuts import render, redirect
from .forms import AuthTableCreationForm
from django.contrib.auth.hashers import make_password
from .forms import LoginForm  # make sure to import your login form
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)


# Home page view. Renders the 'index.html' template and passes the current user to the template context.
def home(request):
    return render(request, 'index.html', {'user': request.user})


# Index view. Renders the 'index.html' template.
def index(request):
    return render(request, 'index.html')


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
                return HttpResponse("User authenticated successfully")
            else:
                return HttpResponse("Invalid username or password")
        else:
            return HttpResponse("Username or password not provided")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Logout view. Logs out the user and redirects to the login page.
def user_logout(request):
    logout(request)
    return redirect('login')


# Create user view. If the request method is POST, it tries to create a new user.
# If the form is valid, it saves the user and redirects to the index page.
# If the request method is not POST, it renders the 'create_user.html' template with an AuthTableCreationForm instance.
def create_user(request):
    if request.method == 'POST':
        form = AuthTableCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('index')
    else:
        form = AuthTableCreationForm()
    return render(request, 'create_user.html', {'form': form})


# Update password view. If the request method is POST, it tries to update the user's password. If the form is valid,
# it saves the new password. If the request method is not POST, it renders the 'update_password.html' template with
# an AuthTablePasswordChangeForm instance.
def update_password(request):
    if request.method == 'POST':
        form = AuthTablePasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AuthTablePasswordChangeForm(request.user)
    return render(request, 'update_password.html', {'form': form})
