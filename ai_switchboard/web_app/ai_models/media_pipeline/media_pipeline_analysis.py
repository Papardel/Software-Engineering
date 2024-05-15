from ..media_processing_interface.video_processor import VideoProcessor
from .mediapipe_app import process_video
import os


class MediaPipelineAnalyser(VideoProcessor):
    def get_directory(self):
        return os.path.dirname(__file__)

    def run_model(self, vid_name):
        # Call the process_video function and pass the video id, video file path, and video name
        process_video(vid_name)

        return f"media_pipeline_output-{vid_name}.mp4"
