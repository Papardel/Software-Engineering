import asyncio
import queue
import re
import threading
import time
import asgiref
import httpx
import requests
from asgiref.sync import async_to_sync, sync_to_async
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone
from ..models import Video

# Set this to the URL of the .m3u8 file provided by your Nginx HLS setup.
nginx_hls_url = "http://192.168.3.249:8080/hls/stream.m3u8"

video_queue = queue.Queue()

def save_video_thread():
    while True:
        video = video_queue.get()  # Get the next video from the queue
        save_video(video)  # Save the video
        video_queue.task_done()  # Indicate that the task is done

def live_feed(request):
    sync_live_feed_logic = async_to_sync(live_feed_logic)
    response = sync_live_feed_logic(request)
    return StreamingHttpResponse(response, content_type='multipart/x-mixed-replace; boundary=frame')


async def live_feed_logic(request):
    print("Accessing live feed from NGINX...")
    video_buffer = []
    frame_count = 0
    desired_frame_count = 5  # Desired frame count

    async for frame in generate_frames("http://192.168.3.249:8080/hls/stream.m3u8"):
        print("Received frame")
        video_buffer.append(frame)
        frame_count += 1
        if frame_count >= desired_frame_count:
            # Add the video buffer to the queue
            video_queue.put(video_buffer)
            video_buffer = []
            frame_count = 0

    return StreamingHttpResponse(iter([]), content_type='multipart/x-mixed-replace; boundary=frame')


async def generate_frames(nginx_hls_url):
    print(f"Attempting to connect to {nginx_hls_url}")
    async with httpx.AsyncClient() as session:
        while True:
            r = await session.get(nginx_hls_url)

            if r.status_code == 200:
                print("Connected successfully")
                content = r.content.decode('utf-8')
                segment_urls = [nginx_hls_url.rsplit('/', 1)[0] + '/' + 'stream-' + segment for segment in
                                re.findall(r'(\w+\.ts)', content)]

                for segment_url in segment_urls:
                    segment_response = await session.get(segment_url)
                    for frame in segment_response.iter_bytes():
                        yield frame

            else:
                print(f"Failed to get stream with status code: {r.status_code}")
                print("Retrying in 5 seconds...")
                print(threading.enumerate())

            await asyncio.sleep(5)  # Add delay before retrying

def save_video(video):
    video_data = b''.join(video)
    new_video = Video.objects.create(
        name=f'Video_{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4',
        data=video_data
    )
    new_video.save()
    print("Video segment saved to database:", new_video.name)


def show_live_stream(request):
    return render(request, 'live_feed.html')
