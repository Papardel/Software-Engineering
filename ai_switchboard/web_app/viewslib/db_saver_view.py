# ai_switchboard/web_app/viewslib/db_saver_view.py
import queue
import threading
from django.utils import timezone
import logging

video_queue = queue.Queue()
logger = logging.getLogger(__name__)


def create_video_object(video_data, name):
    from ..models import Video
    try:
        new_video = Video.objects.create(
            name=f'{name}_{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4',
            data=video_data
        )
        logger.info("Video segment saved to database:", new_video.name)
        return new_video
    except Exception as e:
        logger.error(f"Error saving video: {e}")
        return None


def save_video(video_data, name):
    from ..models import User, Notification
    new_video = create_video_object(video_data, name)
    if new_video is not None:
        new_video.save()
        logger.info("Video segment saved to database:", new_video.name)
        user, _ = User.objects.get_or_create(username="surveillance_system")
        Notification.objects.create(
            is_emergency=True,
            message=f"{name} SUSPICIOUS ACTIVITY. VIDEO SAVED TO DATABASE.",
            user=user
        )
    else:
        logger.info("No video segment saved to database")
