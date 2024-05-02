from django.shortcuts import render
from dotenv import load_dotenv
import os

load_dotenv()


def show_live_stream_view(request):
    hls_url = os.getenv('NGINX_HLS_URL')
    print(f"HLS URL FOR RENDER: {hls_url}")  # Print the HLS URL for debugging
    return render(request, 'live_feed.html', {'hls_url': hls_url})
