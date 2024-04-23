import requests
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone
from ..models import Video

# Set this to the URL of the .m3u8 file provided by your Nginx HLS setup.
nginx_hls_url = "http://192.168.3.249:8080/hls/stream.m3u8"


def generate_frames():
    print(f"Attempting to connect to {nginx_hls_url}")
    r = requests.get(nginx_hls_url, stream=True)
    if r.status_code == 200:
        print("Connected successfully")
        # Handling HLS stream: parse the .m3u8 playlist and manage segment downloads
        for line in r.iter_lines():
            if line and not line.startswith(b'#'):
                # Assuming line is a path to a segment file
                segment_url = nginx_hls_url.rsplit('/', 1)[0] + '/' + line.decode('utf-8')
                segment_response = requests.get(segment_url, stream=True)
                for chunk in segment_response.iter_content(chunk_size=1024):
                    yield chunk
    else:
        print(f"Failed to get stream with status code: {r.status_code}")


def live_feed_logic(request):
    print("Accessing live feed from NGINX...")
    video_buffer = []
    frame_count = 0

    for chunk in generate_frames():
        print("Received chunk")
        video_buffer.append(chunk)
        frame_count += 1
        # Adjust this value according to your segment duration and logic needs
        if frame_count >= 1000:
            save_video(video_buffer)
            video_buffer = []
            frame_count = 0

    return StreamingHttpResponse(iter([]), content_type='multipart/x-mixed-replace; boundary=frame')


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
