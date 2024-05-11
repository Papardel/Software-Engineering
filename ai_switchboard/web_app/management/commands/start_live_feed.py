from django.core.management.base import BaseCommand
from threading import Thread

from ...models import Camera
from ...viewslib.frame_generator_view import live_feed_logic
import asyncio


async def consume_live_feed_logic(camera):
    async for _ in live_feed_logic(camera):
        pass


def start_camera_feed(camera):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(consume_live_feed_logic(camera))


class Command(BaseCommand):
    help = 'Starts the live feed logic'

    def handle(self, *args, **options):
        cameras = Camera.objects.all()
        for camera in cameras:
            Thread(target=start_camera_feed, args=(camera,)).start()