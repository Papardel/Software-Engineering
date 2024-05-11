# ai_switchboard/web_app/apps.py
import sys
import threading
import signal
from django.apps import AppConfig
from django.core.management import call_command
from .viewslib.db_saver_view import save_video_thread  # Import the save_video function from db_saver_view.py


def stop_live_feed(signum, frame):
    print("Stopping live feed...")
    sys.exit(0)


def start_live_feed():
    call_command('start_live_feed')


class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_app'
    saver_thread = None
    thread_lock = threading.Lock()

    def ready(self):
        if 'runserver' in sys.argv:
            signal.signal(signal.SIGINT, stop_live_feed)
            signal.signal(signal.SIGTERM, stop_live_feed)

            with WebAppConfig.thread_lock:
                start_live_feed()  # Call start_live_feed directly

                if WebAppConfig.saver_thread is None:
                    WebAppConfig.saver_thread = threading.Thread(target=save_video_thread)
                    WebAppConfig.saver_thread.daemon = True
                    WebAppConfig.saver_thread.start()
                    print(threading.enumerate())