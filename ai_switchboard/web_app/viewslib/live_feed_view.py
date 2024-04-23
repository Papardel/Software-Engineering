import time
import cv2 as cv
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip
from django.utils import timezone

from ..models import *

import cv2


def find_available_cameras(max_cameras_to_check=10):
    available_cameras = []
    for i in range(max_cameras_to_check):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
        else:
            print(f"Cannot open camera at index {i}. Please ensure that the camera is connected and accessible.")
        cap.release()
        time.sleep(0.1)  # Add a small delay
    return available_cameras


@gzip.gzip_page
def live_feed_logic(request):
    def generate_frames():
        available_cameras = find_available_cameras()
        if not available_cameras:
            return

        cap = cv.VideoCapture(available_cameras[0])

        frame_count = 0
        video_buffer = []
        start_time = time.time()

        while True:
            if time.time() - start_time > 20:
                cap.release()
                break
            ret, frame = cap.read()
            if not ret:
                break

            _, img_encoded = cv.imencode('.jpg', frame)
            video_buffer.append(img_encoded.tobytes())
            frame_count += 1

            if frame_count == 90:
                save_video(video_buffer)
                frame_count = 0
                video_buffer = []

            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n'

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def save_video(video):
    video_data = b''.join(video)
    new_video = Video.objects.create(
        name=f'Video_{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}',
        data=video_data
    )
    new_video.save()


def show_live_stream(request):
    context = {
        'camera_access_script': """
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function(stream) {
                    /* Use the stream */
                })
                .catch(function(err) {
                    /* Handle the error */
                });
        """
    }
    return render(request, 'live_feed.html', context)