from django.contrib.auth import authenticate, login as auth_login, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
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
        content = file.read()

        if file_type == 'image':
            image = Image.objects.create(name=name, data=content)
        elif file_type == 'video':
            video = Video.objects.create(name=name, data=content)
        elif file_type == 'csv':
            csv = CSV.objects.create(name=name, data=content.decode())
        elif file_type == 'json':
            json = JSON.objects.create(name=name, data=content.decode())
        elif file_type == 'text':
            text = Text.objects.create(name=name, data=content.decode())

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
    return render(request, 'download.html', {'files': files, 'fileType': file_type})


def view_file(request, file_id):
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
        return HttpResponse('Invalid file type', status=400)

    response = FileResponse(file.data, as_attachment=True, filename=file.name)
    return response


def download_file(request, file_id):
    file_type = request.GET.get('fileType')
    if file_type == 'image':
        file = Image.objects.get(id=file_id)
        content_type = 'image/jpeg'
    elif file_type == 'video':
        file = Video.objects.get(id=file_id)
        content_type = 'video/mp4'
    elif file_type == 'csv':
        file = CSV.objects.get(id=file_id)
        content_type = 'text/csv'
    elif file_type == 'json':
        file = JSON.objects.get(id=file_id)
        content_type = 'application/json'
    elif file_type == 'text':
        file = Text.objects.get(id=file_id)
        content_type = 'text/plain'
    else:
        return HttpResponse('Invalid file type', status=400)

    response = HttpResponse(file.data, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={file.name}'
    return response
