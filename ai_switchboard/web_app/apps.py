import sys
import threading
import signal
from django.apps import AppConfig
from django.core.management import call_command


def stop_live_feed(signum, frame):
    print("Stopping live feed...")
    sys.exit(0)


def start_live_feed():
    call_command('start_live_feed')


class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_app'

    def ready(self):
        if 'runserver' in sys.argv:
            signal.signal(signal.SIGINT, stop_live_feed)
            signal.signal(signal.SIGTERM, stop_live_feed)
            #start_live_feed()  # Call start_live_feed directly
