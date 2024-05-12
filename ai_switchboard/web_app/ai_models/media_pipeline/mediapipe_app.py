'''
The code used to deploy a mediapipe pose estimation model via an API.
The code returns a json of the skeletal coordinates and no video. The optional
Author: Josh Amoils
Date: 26/09/2023
'''
import logging
import random
import time

import cv2
import mediapipe as mp
import requests
import csv
import os
import tempfile
import boto3
import json
import pandas as pd
import subprocess
from ...models import Video, CSV
from django.core.files import File

logging.basicConfig(level=logging.INFO)

"""
# AWS credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')

# Initialize AWS S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
"""


# Initialize MediaPipe Pose and Drawing utilities
def load_model():
    """
    Load the mediapipe pose estimation model.
    """
    global model
    model = mp.solutions.pose.Pose()


def write_landmarks_to_dict(landmarks, frame_number, dict_data):
    """
    Write the landmarks to a dictionary.

    Args:
        landmarks: The landmarks to write.
        frame_number: The current frame number.
        dict_data: The dictionary to write to.
    """
    for idx, landmark in enumerate(landmarks):
        dict_data['data'].loc[len(dict_data['data'])] = [frame_number, mp.solutions.pose.PoseLandmark(idx).name,
                                                         landmark.x, landmark.y, landmark.z, landmark.visibility]
    return dict_data


def init_video_writer(frame, cap):
    """
    Initialize the video writer.

    Args:
        frame: The current frame.
        cap: The video capture object.
    """
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        video_output_path = temp_file.name

    (frameHeight, frameWidth) = frame.shape[:2]
    h = 500
    w = int((h / frameHeight) * frameWidth)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    writer = cv2.VideoWriter(video_output_path, fourcc, fps, (w, h), True)

    return writer, w, h, video_output_path


def process_video(vid_name, enable_writer=True):
    start_time = time.time()

    logging.info(f'Starting to process video: {vid_name}')
    logging.info(f'Video ID: {vid_name}')
    video_file_path = os.path.join(os.path.dirname(__file__), vid_name)
    logging.info(f'Video file path: {video_file_path}')

    cap = cv2.VideoCapture(video_file_path)
    if cap.isOpened():
        logging.info("Video capture opened successfully")
    else:
        logging.error(f"Failed to open video capture. Error: {cap}")

    frame_number = 0
    dict_data = {
        'video_name': vid_name,
        'video_filepath': '',
        'data': pd.DataFrame(columns=['frame_number', 'keypoint', 'x_coord', 'y_coord', 'z_coord', 'visibility']),
    }
    logging.info("MADE DICT")
    writer = None
    mp_drawing = mp.solutions.drawing_utils
    load_model()
    logging.info("MODEL LOADED")

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = model.process(frame_rgb)

        if result.pose_landmarks:
            write_landmarks_to_dict(result.pose_landmarks.landmark, frame_number, dict_data)

            if enable_writer:
                if writer is None:
                    writer, w, h, video_output_path = init_video_writer(frame, cap)
                else:
                    mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
                    writer.write(cv2.resize(frame, (w, h)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_number += 1

    cap.release()

    if writer is not None:
        writer.release()
        ffmpeg_filename = f"media_pipeline_output-{vid_name}.mp4"
        subprocess.run(['ffmpeg', '-y', '-i', video_output_path, '-vcodec', 'libx264', '-an', ffmpeg_filename])
        dict_data["video_filepath"] = f"{ffmpeg_filename}"

    cv2.destroyAllWindows()

    csv_data = dict_data['data'].to_csv(index=False)
    CSV.objects.create(name=f"media_pipeline_output-{vid_name}.csv", data=csv_data)

    with open(dict_data["video_filepath"], 'rb') as file:  # create video object to save in db
        # Read the file data as bytes
        video_data = file.read()
        # Create a new Video object and save it to the database
        Video.objects.create(name=f"media_pipeline_output-{vid_name}", data=video_data)

    logging.info(f'Finished processing video: {vid_name}')
    if os.path.exists(dict_data["video_filepath"]):
        os.remove(dict_data["video_filepath"])
        logging.info(f'Deleted local output file: {dict_data["video_filepath"]}')
    else:
        logging.error(f'Error deleting local output file: {dict_data["video_filepath"]} File does not exist.')

    if os.path.exists(video_file_path):
        os.remove(video_file_path)
        logging.info(f'Deleted video file: {video_file_path}')
    else:
        logging.error(f'Error deleting video file: {video_file_path} File does not exist.')
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f'The process_video function took {duration} seconds to run.')
    return
