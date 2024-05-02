# ai_switchboard/web_app/viewslib/db_saver_view.py
import queue
import threading
from django.utils import timezone

video_queue = queue.Queue()


def save_video_thread():
    while True:
        video = video_queue.get()
        save_video(video)
        video_queue.task_done()


def save_video(video):
    from ..models import Video  # Move the import statement here
    video_data = b''.join(video)
    new_video = Video.objects.create(
        name=f'Video_{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4',
        data=video_data
    )
    new_video.save()
    print("Video segment saved to database:", new_video.name)


def start_saving_thread():
    save_thread = threading.Thread(target=save_video_thread)
    save_thread.start()