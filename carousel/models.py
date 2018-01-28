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
    color = models.CharField( max_length=100, default='')
    json = JSONField()
    # anable / disable comments
    comments_display = models.CharField( max_length=100, default='block')

class PostComment(models.Model):
    author = models.TextField()
    slide = models.IntegerField(default= 0)
    text = models.TextField()
    lecture = models.TextField()
    class_id = models.ForeignKey( Presentation, on_delete = models.CASCADE)
    # main parent comment
    main = models.ForeignKey('self' , on_delete = models.CASCADE, related_name = '%(class)s_main', blank = True, null=True)
    # actual parent comment
    parent = models.ForeignKey('self', on_delete = models.CASCADE, related_name='%(class)s_parent', blank =True, null=True)
    # thread level
    level = models.IntegerField(default = 0)
    # replied_to
    replied_to = models.CharField(max_length = 100, blank =True, null=True)

    # user tag
    user_tag = models.CharField(max_length = 100, blank =True, null=True)
    # admin tag
    admin_tag = models.CharField(max_length = 100, blank =True, null=True, default= "")
    

    # Time is a rhinocerous
    created = models.DateTimeField(auto_now_add=True)