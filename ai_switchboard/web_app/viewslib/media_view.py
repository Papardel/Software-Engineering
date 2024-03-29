from django.shortcuts import render, redirect
from ..models import *


def media_logic(request):
    file_types = request.GET.getlist('fileType')
    files = []

    if 'image' in file_types or file_types == []:
        images = Image.objects.all()
        for image in images:
            files.append({'id': image.id, 'name': image.name, 'type': 'image'})

    if 'video' in file_types or file_types == []:
        videos = Video.objects.all()
        for video in videos:
            files.append({'id': video.id, 'name': video.name, 'type': 'video'})

    if 'csv' in file_types or file_types == []:
        csv_files = CSV.objects.all()
        for csv_file in csv_files:
            files.append({'id': csv_file.id, 'name': csv_file.name, 'type': 'csv'})

    if 'json' in file_types or file_types == []:
        json_files = JSON.objects.all()
        for json_file in json_files:
            files.append({'id': json_file.id, 'name': json_file.name, 'type': 'json'})

    if 'text' in file_types or file_types == []:
        text_files = Text.objects.all()
        for text_file in text_files:
            files.append({'id': text_file.id, 'name': text_file.name, 'type': 'text'})

    return render(request, 'media.html', {'files': files})


def delete_file_logic(file_id, file_type):
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
    return redirect('media')
