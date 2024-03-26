import base64

from django.http import HttpResponse
from django.shortcuts import render

from ..mediapipe_app import *
from ..models import *

def mediapipe_video_logic(request, vid_name=None):
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
        process_video(video.id, temp_file_path, vid_name)
        return HttpResponse('Video analysis initiated', status=200)