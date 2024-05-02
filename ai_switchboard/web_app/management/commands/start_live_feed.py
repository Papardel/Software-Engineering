# ai_switchboard/web_app/management/commands/start_live_feed.py
from django.core.management.base import BaseCommand
from web_app.viewslib.frame_generator_view import live_feed_logic
import asyncio


# IDK what this does, but it's necessary for the code to work apparently =)
async def consume_live_feed_logic():
    async for _ in live_feed_logic(None):
        pass


class Command(BaseCommand):
    help = 'Starts the live feed logic'

    def handle(self, *args, **options):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(consume_live_feed_logic())
        loop.close()
