from django.shortcuts import render
from dotenv import load_dotenv
import os

from ..models import Camera

load_dotenv()


def show_live_stream_view(request):
    base_hls_url = os.getenv('NGINX_HLS_URL')
    # Fetch all camera names from the database
    cameras = Camera.objects.values_list('name', flat=True)

    # Create a dictionary with camera names as keys and HLS URLs as values
    hls_urls = {camera: base_hls_url.format(camera_name=camera) for camera in cameras}
    print(f"HLS URLs FOR RENDER: {hls_urls}")  # Print the HLS URLs for debugging

    return render(request, 'live_feed.html', {'hls_urls': hls_urls, 'cameras': cameras})
