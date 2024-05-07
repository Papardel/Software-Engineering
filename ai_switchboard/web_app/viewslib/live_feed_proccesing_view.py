import os

from ..ai_models.test_live_stream_ai_processor.audio_analysis import audio_analyser
from .db_saver_view import *

# objective is to have class entities which all implement a run interface and based on the response the video gets saved
ais = [audio_analyser()]  # list of models to run videos through


def stream_processing(video_file_path):
    for model in ais:
        response = model.run_model(video_file_path)
        if response is True:  # eventually this will produce a notification
            with open(video_file_path, 'rb') as file:
                video_data = file.read()
            save_video(video_data)
            break
    os.remove(video_file_path)


def start_live_stream_processing():  # for later
    stream_processing_thread = threading.Thread(target=stream_processing)
    stream_processing_thread.start()
