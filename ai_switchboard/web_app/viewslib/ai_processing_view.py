import os
import base64
import logging

from django.http import HttpResponse
from django.core.serializers import serialize
from django.shortcuts import render, redirect

from ..ai_models.media_pipeline.media_pipeline_analysis import MediaPipelineAnalyser
from ..ai_models.test_video_ai_processing.video_analysis import VideoAnalyser
from ..ai_models.media_processing_interface.media_processor import MediaProcessor
from ..models import *

logger = logging.getLogger(__name__)

"""
Each format of file in the db has a different set of processing models that can be used on it, so we have a dictionary
for each format that maps a dictionary of processing model to the format of the file.
"""
video_processor_dictionary = {'media_pipeline': MediaPipelineAnalyser(), 'video_analysis': VideoAnalyser()}
image_processing_dictionary = {'testing_img_1': 'testing', 'testing_img_2': 'testing'} # for testing purposes
json_processing_dictionary = {'testing_json_1': 'testing', 'testing_json_2': 'testing'} # for testing purposes
csv_processing_dictionary = {'testing_csv_1': 'testing', 'testing_csv_2': 'testing'} # for testing purposes
txt_processing_dictionary = {}

processor_dictionary = {'video': video_processor_dictionary, 'image': image_processing_dictionary,
                        'json': json_processing_dictionary, 'csv': csv_processing_dictionary,
                        'txt': txt_processing_dictionary}

# returns a dictionary of processing models for each file format that has processing models
def get_processing_models():
    return {k: v for k, v in processor_dictionary.items() if v != {}}

# finds the format of a processing model
def find_format(processing_model):
    for data_format, models in processor_dictionary.items():
        if processing_model in models:
            return data_format, models
    return None

# returns the database object based on a data format
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


def default_render(request):
    format_processing_models = get_processing_models()
    formats = list(format_processing_models.keys())
    models = [ {'name': model, 'type': format} for format in formats for model in processor_dictionary[format].keys()]
    media = [{'name': file.name, 'type': format}  for format in formats for file in get_data_format_object(format).objects.all()]
    return render(request, 'process.html', {'formats': formats, 'models': models, 'media': media})

""" 
Based on the available processing methods for each data format, the process.html page will display the available
formats and processing methods for the user to choose from. The user can then select a format and processing method
as well as media of that format to process. 
"""


def ai_processing_logic(request, file_name=None, processing_model=None):
    if file_name and processing_model: 
        data_format, processing_dictionary = find_format(processing_model)
        
        if isinstance(processing_dictionary[processing_model], MediaProcessor):
            # make temp file of file retrieved from db in the directory of the processing model
            get_video__make_temp_file(file_name, processing_dictionary[processing_model].get_directory(), data_format)
            outputs = []
            try:
                """Outputs now should be a list of tuples of the output file name and its data type"""
                ouputs = processing_dictionary[processing_model].run_model(file_name)  # run model
            except Exception as e: # case the processing method in the dictionary doesn't implement the interface
                logger.error(f'Error processing {file_name} with {processing_model}: {e}')
                return HttpResponse(f'Error processing {file_name} with {processing_model}: {e}', status=500)

            output_list = []
            for (output_name, data_format) in ouputs:
                db_object = get_data_format_object(data_format).objects.filter(name=output_name).first()
                output_id = db_object.id
                output_list.append(f'{output_id},{output_name},{data_format}')
            output_string = '|'.join(output_list)

            Notification.objects.create(
                is_read=False,
                message=f'{processing_model} processing complete on {file_name}|{output_string}',
                user=request.user
            )
        else: # for testing extendability I am not running the models other models, just pretending
            logger.info(f'Processing method doesnt implement the interface MediaProcessor')
            
    return default_render(request)  # will only happen when page is first rendered or file was processed
