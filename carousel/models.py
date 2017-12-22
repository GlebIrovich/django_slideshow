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
    def __str__(self):
        return self.name
