# carousel/urls

from django.conf.urls import url
from . import views

app_name = 'carousel'

urlpatterns = [
    # upload
    url(r'^upload/$', views.upload_documents, name= 'upload'),
    # delete
    url(r'^delete/$', views.DeleteList, name='delete'),
    # classes
    url(r'^$', views.list_classes, name='list_classes'),
    # lectures
    url(r'^(?P<class_id>[0-9]+)/$', views.list_lectures, name='list_lectures'),
    # slideshow with subchapters
    url(r'^(?P<class_id>[0-9]+)/(?P<key>.*)/$', views.list_lectures, name='list_lectures'),

    # /
]
