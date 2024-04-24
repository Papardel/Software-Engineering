from django.core.management.base import BaseCommand
from web_app.viewslib.live_feed_view import live_feed_logic
import asyncio


class Command(BaseCommand):
    help = 'Starts the live feed logic'

    def handle(self, *args, **options):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(live_feed_logic(None))
        loop.close()
