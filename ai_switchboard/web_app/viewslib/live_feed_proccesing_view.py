from ai_switchboard.web_app.ai_models.test_live_stream_ai_processor.audio_analysis import audio_analyser
from db_saver_view import *

# objective is to have class entities which all implement a run interface and based on the response the video gets saved
ais = [audio_analyser()]  # list of models to run videos through


def stream_processing(video):
    for model in ais:
        response = model.run_model(video)
        if response:  # eventually this will produce a notification
            save_video(video)
            break


"""
ffmpeg has audio processing 
"""


def start_live_stream_processing():
    stream_processing_thread = threading.Thread(target=stream_processing)
    stream_processing_thread.start()
