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
    # show collapse comments
    url(r'^ajax/toggle_comments/$', views.toggle_comments, name='toggle_comments'),
    # change color
    url(r'^ajax/change_color/$', views.change_color, name='change_color'),

    # lectures
    url(r'^(?P<class_id>[0-9]+)/$', views.ListLectures.as_view(), name='list_lectures'),
    # slideshow with subchapters
    url(r'^(?P<class_id>[0-9]+)/(?P<key>.*)/$', views.ListLectures.as_view(), name='list_lectures'),

    # upload manual
    url(r'^upload_manual/$', views.manual, name= 'manual'),

    

]
