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

# returns a dictionary of processing models for each file format that has processing models
def get_processing_models():
    return {k: v for k, v in processor_dictionary.items() if v != {}}


def find_format(processing_model):
    for data_format in processor_dictionary:
        if processing_model in processor_dictionary[data_format].keys():
            return processor_dictionary[data_format]
    return None


def get_data_format_object(data_format):
    match data_format:
        case 'video':
            return Video
        case 'image':
            return Image
        case 'json':
            return JSON
        case 'csv':
            return CSV
        case 'txt':
            return Text
        case _:
            return None


""" Need to adapt this to create temporary file for different data formats """
def get_video__make_temp_file(file_name, processing_method, data_format):

    """Changed to get files of different formats"""
    # Fetch the file with the given name from the database
    file = get_data_format_object(data_format).objects.get(name=file_name)

    # Define the directory where you want to save the files
    file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ai_models', processing_method)

    # Define the path to the file
    file_path = os.path.join(file_dir, f'{file_name}')

    """ Adapt this part to work with all formats"""
    
    # Write the data to the file
    with open(file_path, 'wb') as file_:
        # Decode the data to bytes if it's a base64 string
        file_data = base64.b64decode(file.data) if isinstance(file.data, str) else file.data
        file_.write(file_data)

    return file_path


def media_format_logic(request):
    format_processing_models = get_processing_models()
    formats = list(format_processing_models.keys())
    def_models = list(format_processing_models[formats[0]].keys())
    def_media = get_data_format_object(formats[0]).objects.all()

    if request.method == 'POST':
        chosen_format = request.POST['fileType']
        models = format_processing_models[chosen_format]
        media = get_data_format_object(chosen_format).objects.all()
        return render(request, 'process.html', {'formats': formats, 'models': models, 'media': media})

    return render(request, 'process.html', {'formats': formats, 'models': def_models, 'media': def_media})


""" 
Based on the available processing methods for each data format, the process.html page will display the available
formats and processing methods for the user to choose from. The user can then select a format and processing method
as well as media of that format to process. 
"""


def ai_processing_logic(request, file_name=None, processing_model=None):
    if file_name is None:
        return media_format_logic(request)
    else:
        processing_dictionary = find_format(processing_model)

        # make temp file of file retrieved from db in the directory of the processing model
        get_video__make_temp_file(file_name, processing_dictionary[processing_model].get_directory(), 'video')
        
        
        output_name = processing_dictionary[processing_model].run_model(file_name)  # run model

        Notification.objects.create(
            message=f'User {request.user.username} processed file {file_name} with {processing_model}',
            user=request.user
        )

        """HTTP Response needs to be changed to a pop notification or a redirect to the media page."""
        return HttpResponse(f'{processing_model} processing complete on {file_name}, check the media section for {output_name}',
                            status=200)
