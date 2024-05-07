from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..models import *


# show all available files in the db
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


# delete selected file
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
        message=f'User {request.user.username} deleted file {file.name}',
        user=request.user
    )
    return redirect('media')


def delete_all_files_logic(request): # delete all selected files
    file_types = request.GET.getlist('fileType')

    if 'image' in file_types or file_types == []:
        Image.objects.all().delete()
    if 'video' in file_types or file_types == []:
        Video.objects.all().delete()
    if 'csv' in file_types or file_types == []:
        CSV.objects.all().delete()
    if 'json' in file_types or file_types == []:
        JSON.objects.all().delete()
    if 'text' in file_types or file_types == []:
        Text.objects.all().delete()

    return redirect('media')


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


def upload_file_logic(request):
    status_message = ""
    if request.method == 'POST':
        file_type = request.POST['fileType']
        if 'file' not in request.FILES:
            status_message = 'No file uploaded'
            return render(request, 'media.html', {'status_message': status_message})
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
            return render(request, 'media.html', {'status_message': status_message})

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
        Notification.objects.create(
            message=f'User {request.user.username} uploaded file {file.name}',
            user=request.user
        )
        return render(request, 'media.html', {'status_message': status_message})
    Notification.objects.create(
        message=f'User {request.user.username} tried to upload bad file',
        user=request.user
        )
    return render(request, 'media.html', {'status_message': status_message})
