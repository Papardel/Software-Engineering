from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .viewslib.camera_manager_view import manage_camera_feed
from .viewslib.notification_view import *
from .viewslib.user_login_view import *
from .viewslib.media_view import *
from .viewslib.ai_processing_view import *
from .viewslib.frame_generator_view import *
from .viewslib.stream_renderer_view import *

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


def user_logout(request):
    return user_logout_logic(request)


@login_required
def process_view(request, file_name=None, processing_model=None):
    return ai_processing_logic(request, file_name, processing_model)


@login_required
def live_feed(request):
    return live_feed_logic(request)


@login_required
def upload_file(request):
    return upload_file_logic(request)


@login_required
def download_file(request, file_id, file_type):
    return download_file_logic(file_id, file_type, request)


@login_required
def media(request):
    return media_logic(request)


@login_required
def delete_file(request, file_id, file_type):
    return delete_file_logic(file_id, file_type, request)


@login_required
def delete_all_files(request, file_types=""):
    return delete_all_files_logic(request, file_types)


@login_required
def show_live_stream(request):
    return show_live_stream_view(request)


@login_required
def notifications(request):
    return emergency_notifications(request)


@login_required
def latest_notification(request):
    return get_latest_notification(request)


@staff_member_required
def manage_camera_feed_acc(request):
    return manage_camera_feed(request)
