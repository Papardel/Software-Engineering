from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=255)
    data = models.ImageField(upload_to='images/')
    date_of_save = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
    name = models.CharField(max_length=255)
    data = models.FileField(upload_to='videos/')
    date_of_save = models.DateTimeField(auto_now_add=True)


class CSV(models.Model):
    name = models.CharField(max_length=255)
    data = models.FileField(upload_to='csvs/')
    date_of_save = models.DateTimeField(auto_now_add=True)


class JSON(models.Model):
    name = models.CharField(max_length=255)
    data = models.FileField(upload_to='jsons/')
    date_of_save = models.DateTimeField(auto_now_add=True)


class Text(models.Model):
    name = models.CharField(max_length=255)
    data = models.FileField(upload_to='texts/')
    date_of_save = models.DateTimeField(auto_now_add=True)
