# carousel/models

from django.db import models
from django.contrib.postgres.fields import JSONField


import os

from .scripts import randomword

def user_directory_path(instance, filename):
    directory = randomword(10)
    return directory + '/' + filename

class Presentation(models.Model):
    title = models.CharField( max_length=100, default='noname')
    docfile = models.FileField(upload_to=user_directory_path)
    json = JSONField()

class PostComment(models.Model):
    author = models.TextField()
    slide = models.IntegerField(default= 0)
    text = models.TextField()
    lecture = models.TextField()
    class_id = models.ForeignKey( Presentation, on_delete = models.CASCADE)


    # Time is a rhinocerous
    created = models.DateTimeField(auto_now_add=True)