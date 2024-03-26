import logging
from django.contrib.auth.decorators import login_required
from .viewslib.user_login_view import *
from .viewslib.download_view import *
from .viewslib.upload_view import *
from .viewslib.media_view import *
from .viewslib.ai_processing_view import *

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

@login_required
def process_video_view(request, vid_name=None):
    return mediapipe_video_logic(request, vid_name)


@login_required
def download_file(request, file_id):
    return download_file_logic(request, file_id)


@login_required
def media(request):
    return media_logic(request)
