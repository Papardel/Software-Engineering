import multiprocessing
import asyncio
import django

from .models import Camera
from .viewslib.frame_generator_view import live_feed_logic


class KillableProcess(multiprocessing.Process):
    def __init__(self, camera_id, *args, **kwargs):
        super(KillableProcess, self).__init__(*args, **kwargs)
        self.camera_id = camera_id

    async def consume_live_feed_logic(self):
        django.setup()
        camera = Camera.objects.get(id=self.camera_id)
        try:
            async for _ in live_feed_logic(camera):
                pass
        except Exception as e:
            print(f"Error in consume_live_feed_logic: {e}")

    def run(self):
        # multiprocessing.set_start_method('fork')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.consume_live_feed_logic())
        finally:
            loop.close()
