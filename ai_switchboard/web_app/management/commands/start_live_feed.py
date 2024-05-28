from django.core.management.base import BaseCommand
from ...models import Camera
from ...threads import KillableProcess


class Command(BaseCommand):
    help = 'Starts the live feed logic'

    def handle(self, *args, **options):
        for camera in Camera.objects.all():
            process = KillableProcess(camera, name=camera.name)
            process.start()
