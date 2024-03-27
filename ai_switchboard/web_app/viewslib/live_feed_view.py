import time
import cv2 as cv
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip

from ..models import *

# tag compresses response as gzip -> streaming data efficiently over network
@gzip.gzip_page
def live_feed_logic(request):

    def generate_frames():
        # 0 for default camera
        cap = cv.VideoCapture(0)
        frame_count = 0
        video_buffer = []
        start_time = time.time()

        while True:
            if time.time() - start_time > 20:
                break
            ret, frame = cap.read()
            # can't receive frame
            if not ret:
                break

            # process frame
            _, img_encoded = cv.imencode('.jpg', frame)
            video_buffer.append(img_encoded.tobytes())
            frame_count += 1

            # save 3-second videos every 90 frames (assuming 30 fps)
            if frame_count == 90:
                save_video(video_buffer)
                frame_count = 0
                video_buffer = []

            # yields encoded frame as a bytes object
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n'

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def save_video(video):
    video_data = b''.join(video)
    new_video = Video.objects.create(data=video_data)
    new_video.save()


def show_live_stream(request):
    return render(request, 'live_feed.html')
