#report/urls

from django.conf.urls import url
from . import views

app_name = 'report'

urlpatterns = [
    # report comment activity
    url(r'^(?P<document_id>[0-9]+)/$', views.report_comments, name='report_comments'),
]
