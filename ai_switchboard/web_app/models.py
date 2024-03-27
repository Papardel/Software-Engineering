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

# Idea is to create a model for each AI model we have
# Model has a name, fileType input and a fileType output

