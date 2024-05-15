# video analysis takes in a video and outputs a some other video
# edge detector
import cv2
import os

from ..media_processing_interface.video_processor import VideoProcessor
from ...models import Video


def detect_edges(video_path, video_name):
    # Creating a VideoCapture object to read the video
    cap = cv2.VideoCapture(video_path)

    # Get the video frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_name = f'edge_detection_output-{video_name}'
    output_file_path = os.path.join(os.path.dirname(__file__), output_name)

    # Define the codec and create a VideoWriter object
    out = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height),
                          isColor=False)
    # Loop until the end of the video
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale for edge detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Using cv2.Canny() for edge detection
        edge_detect = cv2.Canny(gray_frame, 100, 200)

        # Write the edge-detected frame to the output video
        out.write(edge_detect)

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

    print("Edge detection video saved successfully.")
    print("Output file saved to:", os.path.abspath(output_name))

    return output_name, output_file_path


class VideoAnalyser(VideoProcessor):
    def get_directory(self):
        return os.path.dirname(__file__)

    def run_model(self, vid_name):
        print(f'Running video analysis on {vid_name}')

        video_file_path = os.path.join(os.path.dirname(__file__), vid_name)

        # makes a video with edges detected and saves it to current directory
        output_name, output_file_path = detect_edges(video_file_path,vid_name)

        # save the processed video to the database
        with open(output_file_path, 'rb') as file:
            # Read the file data as bytes
            video_data = file.read()
            # Create a new Video object and save it to the database
            Video.objects.create(name=output_name, data=video_data)

        print(f'Finished processing video: {vid_name}')
        # delete the videos from the directory
        os.remove(output_file_path)
        os.remove(video_file_path)

        return output_name
