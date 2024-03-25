import base64
import tempfile

from django.contrib.auth import authenticate, login as auth_login, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
import logging
from . import mediapipe_app
from .forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib import messages
from .mediapipe_app import process_video

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


def upload(request):
    status_message = ""
    if request.method == 'POST':
        file_type = request.POST['fileType']
        if 'file' not in request.FILES:
            status_message = 'No file uploaded'
            return render(request, 'upload.html', {'status_message': status_message})
        file = request.FILES['file']
        name = file.name
        content = file.read()

        extension = name.split('.')[-1]

        extension_to_type = {
            'jpg': 'image',
            'jpeg': 'image',
            'png': 'image',
            'mp4': 'video',
            'avi': 'video',
            'csv': 'csv',
            'json': 'json',
            'txt': 'text',
        }

        if extension not in extension_to_type:
            status_message = 'Invalid file extension'
            return render(request, 'upload.html', {'status_message': status_message})

        if extension_to_type[extension] != file_type:
            status_message = 'File type does not match file extension'
            return render(request, 'upload.html', {'status_message': status_message})

        match file_type:
            case 'image':
                image = Image.objects.create(name=name, data=content)
            case 'video':
                video = Video.objects.create(name=name, data=content)
            case 'csv':
                csv = CSV.objects.create(name=name, data=content.decode())
            case 'json':
                json = JSON.objects.create(name=name, data=content.decode())
            case 'text':
                text = Text.objects.create(name=name, data=content.decode())

        status_message = 'File uploaded successfully'
        return render(request, 'upload.html', {'status_message': status_message})

    return render(request, 'upload.html', {'status_message': status_message})


def download(request):
    file_type = request.GET.get('fileType')

    match file_type:
        case 'image':
            files = Image.objects.all()
        case 'video':
            files = Video.objects.all()
        case 'csv':
            files = CSV.objects.all()
        case 'json':
            files = JSON.objects.all()
        case 'text':
            files = Text.objects.all()
        case _:
            files = []
    return render(request, 'download.html', {'files': files, 'fileType': file_type})


""" MADE FOR FILE DISPLAY ON WEB APP, UNUSED ATM
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
"""


def view_files(request, file_id):
    file_type = request.GET.get('fileType')
    match file_type:
        case 'image':
            file = Image.objects.get(id=file_id)
        case 'video':
            file = Video.objects.get(id=file_id)
            # Call the process_video function and pass the video id and name
            process_video_view(file_id, file.name)
            return HttpResponse('Video analysis initiated', status=200)
        case 'csv':
            file = CSV.objects.get(id=file_id)
        case 'json':
            file = JSON.objects.get(id=file_id)
        case 'text':
            file = Text.objects.get(id=file_id)
        case _:
            return HttpResponse('Invalid file type', status=400)

    response = FileResponse(file.data, as_attachment=True, filename=file.name)
    return response

def process_video_view(request, vid_name=None):
    if vid_name is None:
        # Fetch all video names from the database
        videos = Video.objects.all()
        # Render a template that displays all video names
        return render(request, 'process_video.html', {'videos': videos})
    else:
        # Fetch the video with the given name from the database
        video = Video.objects.get(name=vid_name)

        # Write the video data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Decode the video data to bytes if it's a base64 string
            video_data = base64.b64decode(video.data) if isinstance(video.data, str) else video.data
            temp_file.write(video_data)
            temp_file_path = temp_file.name

        # Call the process_video function and pass the video id, temporary file path, and video name
        mediapipe_app.process_video(video.id, temp_file_path, vid_name)
        return HttpResponse('Video analysis initiated', status=200)


def download_file(request, file_id):
    file_type = request.GET.get('fileType')
    match file_type:
        case 'image':
            file = Image.objects.get(id=file_id)
            content_type = 'image/jpeg'
        case 'video':
            file = Video.objects.get(id=file_id)
            content_type = 'video/mp4'
        case 'csv':
            file = CSV.objects.get(id=file_id)
            content_type = 'text/csv'
        case 'json':
            file = JSON.objects.get(id=file_id)
            content_type = 'application/json'
        case 'text':
            file = Text.objects.get(id=file_id)
            content_type = 'text/plain'
        case _:
            return HttpResponse('Invalid file type', status=400)

    response = HttpResponse(file.data, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={file.name}'
    return response

def media(request):
    file_types = request.GET.getlist('fileType')
    files = []

    if 'image' in file_types or file_types == []:
        images = Image.objects.all()
        for image in images:
            files.append({'name': image.name, 'type': 'image'})

    if 'video' in file_types or file_types == []:
        videos = Video.objects.all()
        for video in videos:
            files.append({'name': video.name, 'type': 'video'})

    if 'csv' in file_types or file_types == []:
        csv_files = CSV.objects.all()
        for csv_file in csv_files:
            files.append({'name': csv_file.name, 'type': 'csv'})

    if 'json' in file_types or file_types == []:
        json_files = JSON.objects.all()
        for json_file in json_files:
            files.append({'name': json_file.name, 'type': 'json'})

    if 'text' in file_types or file_types == []:
        text_files = Text.objects.all()
        for text_file in text_files:
            files.append({'name': text_file.name, 'type': 'text'})

    return render(request, 'media.html', {'files': files})