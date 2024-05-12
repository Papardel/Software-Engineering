import os
import base64

from django.http import HttpResponse
from django.shortcuts import render

from ..ai_models.media_pipeline.media_pipeline_analysis import MediaPipelineAnalyser
from ..ai_models.media_pipeline.mediapipe_app import *
from ..ai_models.test_video_ai_processing.video_analysis import VideoAnalyser
from ..models import *

processor_dictionary = {'media_pipeline': MediaPipelineAnalyser(), 'video_analyser': VideoAnalyser()}


def get_video__make_temp_file(vid_name, processing_method):
    # Fetch the video with the given name from the database
    video = Video.objects.get(name=vid_name)

    # Define the directory where you want to save the video files
    video_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ai_models', processing_method)

    # Define the path to the video file
    video_file_path = os.path.join(video_dir, f'{vid_name}')

    # Write the video data to the file
    with open(video_file_path, 'wb') as video_file:
        # Decode the video data to bytes if it's a base64 string
        video_data = base64.b64decode(video.data) if isinstance(video.data, str) else video.data
        video_file.write(video_data)

    return video_file_path


def ai_processing_logic(request, vid_name=None):
    """
    Only thing that needs to be done is a parameter from the process_view model is passed
    which dictates the processing model to be used
    """
    if vid_name is None:
        # Fetch all video names from the database
        videos = Video.objects.all()
        # Render a template that displays all video names
        return render(request, 'process_video.html', {'videos': videos})
    else:
        """This first commented out section is how it should look like when processing method is passed as an 
        argument."""

        # make temp file of file retrieved from db
        # get_video__make_temp_file(vid_name, processor_dictionary[processing_method].get_directory())
        # output_name = processor_dictionary[processing_method].run_model(vid_name)  # run model

        # make temp file of file retrieved from db
        # get_video__make_temp_file(vid_name, processor_dictionary['media_pipeline'].get_directory())
        # output_name = processor_dictionary['media_pipeline'].run_model(vid_name)  # run model

        # make temp file of file retrieved from db
        get_video__make_temp_file(vid_name, processor_dictionary['video_analyser'].get_directory())
        output_name = processor_dictionary['video_analyser'].run_model(vid_name)  # run model

        Notification.objects.create(
            message=f'User {request.user.username} processed file {vid_name}',
            user=request.user
        )
        return HttpResponse(f'Video analysis complete, check the media section for {output_name}', status=200)
