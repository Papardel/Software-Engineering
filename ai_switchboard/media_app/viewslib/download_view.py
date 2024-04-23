
from django.http import HttpResponse
from ai_switchboard.web_app.models import *

# download selected file
def download_file_logic(file_id, file_type, request):
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

    Notification.objects.create(
        message=f'User {request.user.username} downloaded file {file.name}',
        user=request.user
    )
    return response
