import os

from ..ai_models.test_live_stream_ai_processing.audio_analysis import AudioAnalyser
from .db_saver_view import *

"""
all ais added to the list below should be classes that implement the LiveStreamProcessor interface, as here we work on
processing video files from the live feed and use that information to know if they are worth saving or not

NOTE : LiveStreamProcessor interface's method run_model should return a boolean value, which is used to evaluate whether
a live stream segment should be saved or not.

"""
video_processing_ais = [AudioAnalyser()]  # list of models to run videos through


def stream_processing(video_file_path, name):
    for model in video_processing_ais:
        """
        Change to 
        response = True  ==>> to test system
        response = model.run_model(video_file_path) ==>> to actually run the models
        """

        response = True  #model.run_model(video_file_path)
        if response is True:
            with open(video_file_path, 'rb') as file:
                video_data = file.read()
            save_video(video_data, name)
            break
    os.remove(video_file_path)

