'''
This is the base mediapipe pose estimation pipeline. It takes an input video and returns a csv file of skeletal points.
This script also has a video writer which can be optionally generated.
Author: Josh Amoils
Date: 26/09/2023
'''

import cv2
import time
import mediapipe as mp
import csv


def write_landmarks_to_csv(landmarks, frame_number, csv_data):
    print(f"Landmark coordinates for frame {frame_number}:")
    for idx, landmark in enumerate(landmarks):
        # print(f"{mp_pose.PoseLandmark(idx).name}: (x: {landmark.x}, y: {landmark.y}, z: {landmark.z})")
        csv_data.append([frame_number, mp_pose.PoseLandmark(idx).name, landmark.x, landmark.y, landmark.z])
    # print("\n")


video_path = './media/input/actual_baby.mp4'
output_csv = './media/output/actual_baby_output.csv'

# Initialize MediaPipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Open the video file
cap = cv2.VideoCapture(video_path)

frame_number = 0
csv_data = []

# Runtime
start_time = time.time()
writer = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Video writer
    if writer is None:
        (frameHeight, frameWidth) = frame.shape[:2]
        h = 500
        w = int((h / frameHeight) * frameWidth)
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        writer = cv2.VideoWriter('./media/output/josh_baby_mediapipe_output.mp4', fourcc, fps, (w, h), True)
    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Pose
    result = pose.process(frame_rgb)

    # Draw the pose landmarks on the frame
    if result.pose_landmarks:
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Add the landmark coordinates to the list and print them
        write_landmarks_to_csv(result.pose_landmarks.landmark, frame_number, csv_data)

    # Write video
    writer.write(cv2.resize(frame, (w, h)))

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_number += 1

cap.release()
writer.release()
cv2.destroyAllWindows()

end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time)

# Save the CSV data to a file
with open(output_csv, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['frame_number', 'landmark', 'x', 'y', 'z'])
    csv_writer.writerows(csv_data)