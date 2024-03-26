from django.http import HttpResponse
from django.shortcuts import render

from ..models import *


def download_logic(request):
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


def download_file_logic(request, file_id):
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
