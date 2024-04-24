from time import timezone

from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=255)
    data = models.BinaryField()
    date_of_save = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
    name = models.CharField(max_length=255)
    data = models.BinaryField()
    date_of_save = models.DateTimeField(auto_now_add=True)


class CSV(models.Model):
    name = models.CharField(max_length=255)
    data = models.TextField()
    date_of_save = models.DateTimeField(auto_now_add=True)


class JSON(models.Model):
    name = models.CharField(max_length=255)
    data = models.TextField()
    date_of_save = models.DateTimeField(auto_now_add=True)


class Text(models.Model):
    name = models.CharField(max_length=255)
    data = models.TextField()
    date_of_save = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    is_emergency = models.BooleanField(default=False)
    message = models.TextField()
    time_of_save = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Idea is to create a model for each AI model we have
# Model has a name, fileType input and a fileType output
