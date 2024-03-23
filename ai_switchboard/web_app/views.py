from django.contrib.auth import authenticate, login as auth_login, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
import logging
from django.contrib.auth import login
from .forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate
from .models import *

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


def upload_file(request):
    if request.method == 'POST':
        file_type = request.POST['fileType']
        file = request.FILES['file']
        name = file.name

        print(f"File type: {file_type}")  # Debug print
        print(f"File name: {name}")  # Debug print

        if file_type == 'image':
            image = Image.objects.create(name=name, data=file)
            print(f"Image object: {image}")  # Debug print
        elif file_type == 'video':
            video = Video.objects.create(name=name, data=file)
            print(f"Video object: {video}")  # Debug print
        elif file_type == 'csv':
            csv = CSV.objects.create(name=name, data=file)
            print(f"CSV object: {csv}")  # Debug print
        elif file_type == 'json':
            json = JSON.objects.create(name=name, data=file)
            print(f"JSON object: {json}")  # Debug print
        elif file_type == 'text':
            text = Text.objects.create(name=name, data=file)
            print(f"Text object: {text}")  # Debug print

        return redirect('index')

    return render(request, 'index.html')


def download(request):
    file_type = request.GET.get('fileType')
    if file_type == 'image':
        files = Image.objects.all()
    elif file_type == 'video':
        files = Video.objects.all()
    elif file_type == 'csv':
        files = CSV.objects.all()
    elif file_type == 'json':
        files = JSON.objects.all()
    elif file_type == 'text':
        files = Text.objects.all()
    else:
        files = []
    return render(request, 'download.html', {'files': files})


def download_file(request, file_id):
    file_type = request.GET.get('fileType')
    if file_type == 'image':
        file = Image.objects.get(id=file_id)
    elif file_type == 'video':
        file = Video.objects.get(id=file_id)
    elif file_type == 'csv':
        file = CSV.objects.get(id=file_id)
    elif file_type == 'json':
        file = JSON.objects.get(id=file_id)
    elif file_type == 'text':
        file = Text.objects.get(id=file_id)
    else:
        return HttpResponseNotFound("File not found.")
    response = FileResponse(file.content, as_attachment=True, filename=file.name)
    return response
