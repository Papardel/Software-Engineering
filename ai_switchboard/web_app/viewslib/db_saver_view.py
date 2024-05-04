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


def create_video_object(video_path):
    from ..models import Video  # Move the import statement here
    try:
        with open(video_path, 'rb') as file:
            video_data = file.read()
        new_video = Video.objects.create(
            name=f'Video_{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4',
            data=video_data
        )
        return new_video
    except Exception as e:
        print(f"Error saving video: {e}")
        return None


def save_video(video_path):
    new_video = create_video_object(video_path)
    if new_video is not None:
        new_video.save()
        print("Video segment saved to database:", new_video.name)
    else:
        print("Error saving video segment to database")


def start_saving_thread():
    save_thread = threading.Thread(target=save_video_thread)
    save_thread.start()
