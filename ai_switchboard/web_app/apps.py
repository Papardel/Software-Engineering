# ai_switchboard/web_app/apps.py
import sys
import threading
import signal
from django.apps import AppConfig
from django.core.management import call_command


def stop_live_feed(signum, frame):
    # Stop the live feed here
    # You might need to modify this part based on how your live feed can be stopped
    print("Stopping live feed...")
    sys.exit(0)


def start_live_feed():
    # Start the live feed
    call_command('start_live_feed')


class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_app'
    live_feed_thread = None
    saver_thread = None
    thread_lock = threading.Lock()

    def ready(self):
        if 'runserver' in sys.argv:
            # Handle SIGINT and SIGTERM signals
            signal.signal(signal.SIGINT, stop_live_feed)
            signal.signal(signal.SIGTERM, stop_live_feed)

            with WebAppConfig.thread_lock:
                # Only start the live feed thread if it hasn't been started yet
                if WebAppConfig.live_feed_thread is None:
                    from .viewslib.live_feed_view import save_video_thread  # Import here to avoid circular import
                    WebAppConfig.live_feed_thread = threading.Thread(target=start_live_feed)
                    WebAppConfig.live_feed_thread.daemon = True
                    WebAppConfig.live_feed_thread.start()

                if WebAppConfig.saver_thread is None:
                    WebAppConfig.saver_thread = threading.Thread(target=save_video_thread)
                    WebAppConfig.saver_thread.daemon = True
                    WebAppConfig.saver_thread.start()
                    print(threading.enumerate())

