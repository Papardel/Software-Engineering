# ai_switchboard/web_app/apps.py
import sys
import threading
import signal
from django.apps import AppConfig
from django.core.management import call_command
from web_app.viewslib.db_saver_view import save_video_thread  # Import the save_video function from db_saver_view.py



def stop_live_feed(signum, frame):
    print("Stopping live feed...")
    sys.exit(0)

def start_live_feed():
    call_command('start_live_feed')

class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_app'
    live_feed_thread = None
    saver_thread = None
    thread_lock = threading.Lock()

    def ready(self):
        if 'runserver' in sys.argv:
            signal.signal(signal.SIGINT, stop_live_feed)
            signal.signal(signal.SIGTERM, stop_live_feed)

            with WebAppConfig.thread_lock:
                if WebAppConfig.live_feed_thread is None:
                    WebAppConfig.live_feed_thread = threading.Thread(target=start_live_feed)
                    WebAppConfig.live_feed_thread.daemon = True
                    WebAppConfig.live_feed_thread.start()

                if WebAppConfig.saver_thread is None:
                    # Use save_video as the target for the saver_thread
                    WebAppConfig.saver_thread = threading.Thread(target=save_video_thread)
                    WebAppConfig.saver_thread.daemon = True
                    WebAppConfig.saver_thread.start()
                    print(threading.enumerate())