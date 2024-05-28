from ..media_processing_interface.video_processor import VideoProcessor
from .mediapipe_app import process_video
import os


class MediaPipelineAnalyser(VideoProcessor):
    def get_directory(self):
        return os.path.dirname(__file__)

    def run_model(self, video_file):
        # Call the process_video function and pass the video id, video file path, and video name
        process_video(video_file)

        output_video = f"media_pipeline_output-{video_file}.mp4"
        output_csv = f"{output_video}.csv"
        return [(output_video, 'video'),(output_csv, 'csv')]
