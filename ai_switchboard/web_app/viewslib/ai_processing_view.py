import os
import base64

from django.http import HttpResponse
from django.shortcuts import render, redirect

from ..ai_models.media_pipeline.media_pipeline_analysis import MediaPipelineAnalyser
from ..ai_models.media_pipeline.mediapipe_app import *
from ..ai_models.test_video_ai_processing.video_analysis import VideoAnalyser
from ..models import *

"""
Each format of file in the db has a different set of processing models that can be used on it, so we have a dictionary
for each format that maps a dictionary of processing model to the format of the file.
"""
video_processor_dictionary = {'media_pipeline': MediaPipelineAnalyser(), 'video_analysis': VideoAnalyser()}
image_processing_dictionary = {}
json_processing_dictionary = {}
csv_processing_dictionary = {}
txt_processing_dictionary = {}

processor_dictionary = {'video': video_processor_dictionary, 'image': image_processing_dictionary,
                        'json': json_processing_dictionary, 'csv': csv_processing_dictionary,
                        'txt': txt_processing_dictionary}


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


def media_format_logic(request):
    if request.method == 'POST':
        media = request.POST['fileType']

        if media is None:
            return render(request, 'process.html')
        else:
            match media:
                case 'video':
                    return render(request, 'process.html', {'media': Video.objects.all(),
                                                            'models': video_processor_dictionary.keys()})
                case 'image':
                    return render(request, 'process.html', {'media': Image.objects.all(),
                                                            'models': image_processing_dictionary.keys()})
                case 'json':
                    return render(request, 'process.html', {'media': JSON.objects.all(),
                                                            'models': json_processing_dictionary.keys()})
                case 'csv':
                    return render(request, 'process.html', {'media': CSV.objects.all(),
                                                            'models': csv_processing_dictionary.keys()})
                case 'txt':
                    return render(request, 'process.html', {'media': Text.objects.all(),
                                                            'models': txt_processing_dictionary.keys()})
                case _:
                    return render(request, 'process.html')
    return render(request, 'process.html')


""" 
Later we will need to handle the case where the user clicks on the file when no processing
method is selected and hence a popup shows up or a message is displayed to the user. Another option is to 
only display file_types which have processing methods available.
"""


def ai_processing_logic(request, file_name=None, processing_model=None):
    if file_name is None:
        """Later we will include the data_type format which conditions the rest but right now, everything is a video."""
        # return media_format_logic(request)
        videos = Video.objects.all()
        return render(request, 'process.html', {'media': videos,
                                                'models': video_processor_dictionary.keys()})
    else:
        """
        Eventually the dictionary used below will by the format chosen by the user and from there a subset 
        of processing methods will be provided to the user to choose from. 
        """
        # make temp file of file retrieved from db
        get_video__make_temp_file(file_name, video_processor_dictionary[processing_model].get_directory())
        output_name = video_processor_dictionary[processing_model].run_model(file_name)  # run model

        Notification.objects.create(
            message=f'User {request.user.username} processed file {file_name}',
            user=request.user
        )
        return HttpResponse(f'{processing_model} processing complete, check the media section for {output_name}',
                            status=200)
