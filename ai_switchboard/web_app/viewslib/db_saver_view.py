import queue
import threading
from django.utils import timezone

video_queue = queue.Queue()


def save_video_thread():
    while True:
        video = video_queue.get()
        save_video(video)
        video_queue.task_done()


def create_video_object(video_data, name):
    from ..models import Video
    try:
        new_video = Video.objects.create(
            name=f'{name}_{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4',
            data=video_data
        )
        return new_video
    except Exception as e:
        print(f"Error saving video: {e}")
        return None


def save_video(video_data, name):
    from ..models import User, Notification
    new_video = create_video_object(video_data, name)
    if new_video is not None:
        new_video.save()
        print("Video segment saved to database:", new_video.name)
        user, flag = User.objects.get_or_create(username="surveillance_system")
        Notification.objects.create(
            is_emergency=True,
            message=f"{name} SUSPICIOUS ACTIVITY. VIDEO SAVED TO DATABASE.",
            user=user
        )


def start_saving_thread():
    save_thread = threading.Thread(target=save_video_thread)
    save_thread.start()