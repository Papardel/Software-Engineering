import asyncio
import os
import re
import tempfile

import httpx
import threading
from asgiref.sync import async_to_sync, sync_to_async
from django.http import StreamingHttpResponse
from dotenv import load_dotenv
from .db_saver_view import save_video
from .live_feed_proccesing_view import stream_processing
import logging

load_dotenv()
hls_url_template = os.getenv('NGINX_HLS_URL')
processed_segments = set()
logger = logging.getLogger(__name__)


async def live_feed_logic(camera):
    video_buffer = []
    frame_count = 0
    desired_segment_count = 1

    nginx_hls_url = hls_url_template.format(camera_name=camera.name)
    logger.info(f"HLS URL FOR RENDER: {nginx_hls_url}")

    async for frame in generate_frames(nginx_hls_url):
        logger.info("Received frame")
        video_buffer.append(frame)
        frame_count += 1
        if frame_count >= desired_segment_count:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp:
                temp.write(b''.join(video_buffer))  # make a temporary file with the video data
            await sync_to_async(stream_processing)(temp.name, camera.name)  # handle stream_processing
            video_buffer = []
            frame_count = 0

    yield StreamingHttpResponse(iter([]), content_type='multipart/x-mixed-replace; boundary=frame')


async def generate_frames(nginx_hls_url):
    logger.info(f"Attempting to connect to {nginx_hls_url}")
    async with httpx.AsyncClient() as session:
        while True:
            response = await session.get(nginx_hls_url)
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                # Extract segment file names with the "stream-" prefix and build their full URLs
                segment_urls = [nginx_hls_url.rsplit('/', 1)[0] + '/' + segment
                                for segment in re.findall(r'(stream-\w+\.ts)', content)]

                for segment_url in segment_urls:
                    # Skip this segment if it has already been processed
                    if segment_url in processed_segments:
                        continue

                    # Process the segment and add it to the processed list
                    segment_response = await session.get(segment_url)
                    if segment_response.status_code == 200:
                        for frame in segment_response.iter_bytes():
                            yield frame
                        processed_segments.add(segment_url)
                    else:
                        logger.info(f"Failed to fetch segment: {segment_url}")

            else:
                logger.error(f"Failed to get playlist with status code: {response.status_code}, retrying in 5 seconds...")
            await asyncio.sleep(5)
