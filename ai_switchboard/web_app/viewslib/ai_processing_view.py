import os
import base64

from django.http import HttpResponse
from django.shortcuts import render

from ..ai_models.media_pipeline.mediapipe_app import *
from ..models import *


def mediapipe_video_logic(request, vid_name=None, output_name=None):
    if vid_name is None:
        # Fetch all video names from the database
        videos = Video.objects.all()
        # Render a template that displays all video names
        return render(request, 'process_video.html', {'videos': videos})
    else:
        # Fetch the video with the given name from the database
        video = Video.objects.get(name=vid_name)

        # Define the directory where you want to save the video files
        video_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ai_models', 'media_pipeline')

        # Define the path to the video file
        video_file_path = os.path.join(video_dir, f'{vid_name}')

        # Write the video data to the file
        with open(video_file_path, 'wb') as video_file:
            # Decode the video data to bytes if it's a base64 string
            video_data = base64.b64decode(video.data) if isinstance(video.data, str) else video.data
            video_file.write(video_data)

        # Call the process_video function and pass the video id, video file path, and video name
        process_video(vid_name, output_name)
        return HttpResponse('Video analysis complete, check the media section for output-"selected file name"', status=200)