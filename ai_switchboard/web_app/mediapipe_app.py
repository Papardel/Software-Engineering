'''
The code used to deploy a mediapipe pose estimation model via an API.
The code returns a json of the skeletal coordinates and no video. The optional
Author: Josh Amoils
Date: 26/09/2023
'''

import random
import cv2
import mediapipe as mp
import requests
import csv
from flask import Flask, jsonify, request
import os
import tempfile
import boto3
import json
import pandas as pd
import subprocess

model = None
app = Flask(__name__)
app.debug = True
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


# Initialize MediaPipe Pose and Drawing utilities
def load_model():
    global model
    model = mp.solutions.pose.Pose()


def write_landmarks_to_dict(landmarks, frame_number, dict_data):
    # keypoints = {}
    for idx, landmark in enumerate(landmarks):
        # keypoints[mp.solutions.pose.PoseLandmark(idx).name] = {'x' : landmark.x, 'y' : landmark.y, 'z' : landmark.z}
        dict_data['data'].loc[len(dict_data['data'])] = [frame_number, mp.solutions.pose.PoseLandmark(idx).name,
                                                         landmark.x, landmark.y, landmark.z, landmark.visibility]
    # dict_data['data'].append({'frame_number' : frame_number, 'keypoints' : keypoints})
    return dict_data


def init_video_writer(frame, cap):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        video_output_path = temp_file.name

    # Params
    (frameHeight, frameWidth) = frame.shape[:2]
    h = 500
    w = int((h / frameHeight) * frameWidth)

    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    writer = cv2.VideoWriter(video_output_path, fourcc, fps, (w, h), True)

    return writer, w, h, video_output_path


def process_video(video_path, vid_name, enable_writer=True):
    cap = cv2.VideoCapture(video_path)

    frame_number = 0
    # Initialise data_dict
    dict_data = {
        'video_name': vid_name,
        'video_filepath': '',
        'data': pd.DataFrame(columns=['frame_number', 'keypoint', 'x_coord', 'y_coord', 'z_coord', 'visibility']),
    }

    writer = None
    mp_drawing = mp.solutions.drawing_utils

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        result = model.process(frame_rgb)

        if result.pose_landmarks:
            # Add the landmark coordinates to the list and print them
            write_landmarks_to_dict(result.pose_landmarks.landmark, frame_number, dict_data)

            # Video writer
            if enable_writer:
                if writer is None:
                    writer, w, h, video_output_path = init_video_writer(frame, cap)
                else:
                    # Draw landmarks on image
                    mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

                    # Write video
                    writer.write(cv2.resize(frame, (w, h)))

        # Exit if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_number += 1

    cap.release()
    if writer is not None:
        writer.release()
        # Convert the file to mp4 using the H264 codec
        ffmpeg_filename = f"output-{random.randint(0, 100000000)}.mp4"
        subprocess.run(['ffmpeg', '-y', '-i', video_output_path, '-vcodec', 'libx264', '-an', ffmpeg_filename])
        # Upload to S3
        dict_data["video_filepath"] = f"{ffmpeg_filename}"
        s3.upload_file(ffmpeg_filename, AWS_S3_BUCKET_NAME, f'{ffmpeg_filename}',
                       ExtraArgs={'ContentType': 'video/mp4'})
        # Delete temporary file
        os.remove(video_output_path)
        os.remove(ffmpeg_filename)
    cv2.destroyAllWindows()

    return dict_data


@app.route('/predict', methods=['POST'])
# predict indicates the URL path that is assosciated with the get_predction function.
# 'methods = ['POST']' specifies that the get_prediction function will only respond when a POST request is made to '/predict' URL.
def get_prediction():
    if request.method == 'POST':  # This line isn't needed but is good practice for readability and error-handling (e.g. what if another HTTP request type (GET) is sent to '/predict'?)
        data = request.get_json()
        file_location = data.get('file_location')
        callback_url = data.get('callback_url')
        if file_location is None:
            return jsonify({'error': 'No video location part'}), 400

        # Download video file from s3
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            s3.download_file(AWS_S3_BUCKET_NAME, file_location, tmp_file.name)

        payload = process_video(tmp_file.name,
                                os.path.basename(tmp_file.name))  # Add extra 'True' parameter to write video

        # Save CSV file data
        csv_buffer = payload['data'].to_csv(index=False)
        csv_file_path = f"AI_SB_{os.path.basename(tmp_file.name).replace('mp4', 'csv')}"
        s3.put_object(Bucket=AWS_S3_BUCKET_NAME, Key=f"{csv_file_path}", Body=csv_buffer)

        if callback_url:
            update_callback(callback_url, payload["video_filepath"], csv_file_path)

        # response_data = {'message': 'Video processed successfully', 'output_data' : payload}
        return jsonify(), 200


def update_callback(url, video_path, result_path):
    headers = {"Content-type": "application/json"}
    data = json.dumps(
        {
            "video_file": video_path,
            "result_file": result_path,
        }
    )
    try:
        requests.post(url, data=data, headers=headers)
    except Exception as e:
        print(e)


if __name__ == '__main__':  # This code only runs if app.py is run directly, everything else will run if app.py is imported.
    load_model()  # load model at the beginning once only

    # Testing
    # video = '/Users/joshuaamoils/Documents/Career/Neolook/ODE/ai_switchboard/media/input/actual_baby.mp4'
    # print(process_video(video))

    app.run(host='0.0.0.0', port=8090)
