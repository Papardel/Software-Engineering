
from django.shortcuts import render, redirect
from multiprocessing import active_children as multiprocessing_active_children

from web_app.forms import CameraFeedForm
from web_app.models import Camera
from web_app.threads import KillableProcess


def manage_camera_feed(request):
    form = CameraFeedForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        camera_name = form.cleaned_data['camera']
        action = form.cleaned_data['action']

        if action == 'start':
            for process in multiprocessing_active_children():
                if process.name == camera_name and isinstance(process, KillableProcess):
                    print(f"A process for camera {camera_name} is already running.")
                    return redirect('manage_camera_feed')
            process = KillableProcess(Camera.objects.get(name=camera_name), name=camera_name)
            process.start()
        elif action == 'stop':
            for process in multiprocessing_active_children():
                if process.name == camera_name and isinstance(process, KillableProcess):
                    process.terminate()
        return redirect('manage_camera_feed')
    return render(request, 'manage_camera_feed.html', {'form': form})
