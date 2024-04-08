
from django.shortcuts import redirect
from ..models import *


def delete_file_logic(file_id, file_type, request):
    match file_type:
        case 'image':
            file = Image.objects.get(id=file_id)
        case 'video':
            file = Video.objects.get(id=file_id)
        case 'csv':
            file = CSV.objects.get(id=file_id)
        case 'json':
            file = JSON.objects.get(id=file_id)
        case 'text':
            file = Text.objects.get(id=file_id)
        case _:
            return
    file.delete()
    Notification.objects.create(
        message=f'User {request.user.username} downloaded file {file.name}',
        user=request.user
    )
    return redirect('media')
