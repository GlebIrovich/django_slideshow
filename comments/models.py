#comments/models

from django.db import models
from carousel.models import Presentation
from slider.settings import AUTH_USER_MODEL as User

class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT,related_name="author",to_field='username')
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