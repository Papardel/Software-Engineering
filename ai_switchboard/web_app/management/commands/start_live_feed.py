from django.core.management.base import BaseCommand
from web_app.models import Camera
from web_app.threads import KillableProcess


class Command(BaseCommand):
    help = 'Starts the live feed logic'

    def handle(self, *args, **options):
        for camera in Camera.objects.all():
            process = KillableProcess(camera, name=camera.name)
            process.start()
