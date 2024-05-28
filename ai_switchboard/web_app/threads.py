import multiprocessing
import django
import asyncio

from .models import Camera
from .viewslib.frame_generator_view import live_feed_logic


class KillableProcess(multiprocessing.Process):
    def __init__(self, camera_id, *args, **kwargs):
        super(KillableProcess, self).__init__(*args, **kwargs)
        self.camera_id = camera_id

    async def consume_live_feed_logic(self):
        try:
            camera = Camera.objects.get(id=self.camera_id)
            async for _ in live_feed_logic(camera):
                pass
        except Exception as e:
            print(f"Error in consume_live_feed_logic: {e}")

    def run(self):
        django.setup()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.consume_live_feed_logic())
        finally:
            loop.close()
