#comments/urls

from django.conf.urls import url
from . import views

app_name = 'comments'

urlpatterns = [
    # create post
    url(r'^ajax/post/$', views.create_post, name='create_post'),
    # delete post
    url(r'^ajax/delete/$', views.delete_post, name='create_post'),
    # show reply form
    url(r'^ajax/show_reply_form/$', views.show_reply_form, name='show_reply_form'),
    # show reply form
    url(r'^ajax/reply/$', views.reply, name='reply'),
    # show admin tag
    url(r'^ajax/admin_tag/$', views.admin_tag, name='admin_tag'),
]
