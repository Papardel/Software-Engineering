import base64
import tempfile
import logging

from django.contrib.auth.decorators import login_required

from . import mediapipe_app
from .viewslib.user_login_view import *
from .viewslib.download_view import *
from .viewslib.upload_view import *
from .viewslib.media_view import *

logger = logging.getLogger(__name__)


@login_required
def landing_page(request):
    return render(request, 'index.html')


def login_required_view(request):
    return render(request, 'login_required.html')


# Index view. Renders the 'gateway.html' template.
def gateway(request):
    return render(request, 'gateway.html')


def user_login(request):
    return user_login_logic(request)


def create_user(request):
    return create_user_logic(request)


def user_logout(request):
    return user_logout_logic(request)


@login_required
def upload(request):
    return upload_logic(request)


@login_required
def download(request):
    return download_logic(request)


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

""" Unused for now
@login_required
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
"""


@login_required
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


@login_required
def download_file(request, file_id):
    return download_file_logic(request, file_id)


@login_required
def media(request):
    return media_logic(request)
