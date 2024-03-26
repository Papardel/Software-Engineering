from django.shortcuts import render
from ..models import *


def upload_logic(request):
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
