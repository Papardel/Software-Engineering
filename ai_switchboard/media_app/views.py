
from .viewslib.media_view import *
from .viewslib.upload_view import *
from .viewslib.download_view import *
from .viewslib.delete_view import *


def upload_file(request):
    return upload_file_logic(request)


def download_file(request, file_id, file_type):
    return download_file_logic(file_id, file_type, request)


def delete_file(request, file_id):
    return delete_file_logic(file_id, request)


def media(request):
    return media_logic(request)
