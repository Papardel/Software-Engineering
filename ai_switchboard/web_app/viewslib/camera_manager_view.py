from django.shortcuts import render, redirect
from multiprocessing import Process, active_children, set_start_method
from ..forms import CameraFeedForm
from ..models import Camera
import asyncio


def run_camera_feed(camera):
    set_start_method('fork')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        from .frame_generator_view import live_feed_logic

        async def consume_live_feed_logic():
            try:
                async for _ in live_feed_logic(camera):
                    pass
            except Exception as e:
                print(f"Error in consume_live_feed_logic: {e}")

        loop.run_until_complete(consume_live_feed_logic())
    finally:
        loop.close()


def manage_camera_feed(request):
    form = CameraFeedForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        camera_name = form.cleaned_data['camera']
        action = form.cleaned_data['action']

        if action == 'start':
            if any(p.name == camera_name for p in active_children()):
                print(f"A process for camera {camera_name} is already running.")
                return redirect('manage_camera_feed')

            camera = Camera.objects.get(name=camera_name)
            process = Process(target=run_camera_feed, args=(camera,))
            process.name = camera_name
            process.start()

        elif action == 'stop':
            for process in active_children():
                if process.name == camera_name:
                    process.terminate()
                    process.join()

        elif action == 'start all':
            for camera in Camera.objects.all():
                if not any(p.name == camera.name for p in active_children()):
                    process = Process(target=run_camera_feed, args=(camera,))
                    process.name = camera.name
                    process.start()

        elif action == 'kill all':
            for process in active_children():
                process.terminate()
                process.join()

        return redirect('manage_camera_feed')
    return render(request, 'manage_camera_feed.html', {'form': form})
