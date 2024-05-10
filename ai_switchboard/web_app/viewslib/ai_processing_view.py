import os
import base64

from django.http import HttpResponse
from django.shortcuts import render

from ..ai_models.media_pipeline.mediapipe_app import *
from ..models import *


def get_video(vid_name):
    if vid_name is None:
        video = None
    else:
        # Fetch the video with the given name from the database
        video = Video.objects.get(name=vid_name)
    return video


def decode(video, vid_name, model_dir):
    video_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ai_models', model_dir)

    # Define the path to the video file
    video_file_path = os.path.join(video_dir, f'{vid_name}')

    # Write the video data to the file
    with open(video_file_path, 'wb') as video_file:
        # Decode the video data to bytes if it's a base64 string
        video_data = base64.b64decode(video.data) if isinstance(video.data, str) else video.data
        video_file.write(video_data)


def ai_processing_logic(request, vid_name=None, output_name=None):
    """ add model parameter to the function
    if model == "media_pipe":
        return mediapipe_video_logic(request, vid_name, output_name)
    elif model == "video_analysis":
        return video_analysis_logic(request, vid_name, output_name)
    """
    # No model selected
    return mediapipe_video_logic(request, vid_name, output_name)


def video_analysis_logic(request, vid_name=None, output_name=None):
    video = get_video(vid_name)

    # Define the directory where you want to save the video files and decode video_data
    decode(video, vid_name, 'test_video_ai_processing')

    # Call the process_video function and pass the video id, video file path, and video name
    # process_video(vid_name, output_name)  # change here

    Notification.objects.create(
        message=f'User {request.user.username} processed file {vid_name}',
        user=request.user
    )
    return HttpResponse('Video analysis complete, check the media section for output-"selected file name"', status=200)


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
        Notification.objects.create(
            message=f'User {request.user.username} processed file {vid_name}',
            user=request.user
        )
        return HttpResponse('Video analysis complete, check the media section for output-"selected file name"',
                            status=200)