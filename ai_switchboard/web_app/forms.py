from django import forms
from .models import Camera


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CameraFeedForm(forms.Form):
    camera = forms.ChoiceField(choices=[])
    action = forms.ChoiceField(choices=[('start', 'start'), ('stop', 'stop'), ('start all', 'start all'), ('kill all', 'kill all')])

    def __init__(self, *args, **kwargs):
        super(CameraFeedForm, self).__init__(*args, **kwargs)
        cameras = Camera.objects.all()
        if cameras:
            self.fields['camera'].choices = [(camera.name, camera.name) for camera in cameras]
        else:
            self.fields['camera'].choices = []
