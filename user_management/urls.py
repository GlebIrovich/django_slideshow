#user_management/urls

from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user_management'

urlpatterns = [
    url(r'^accounts/signup/student/$', views.StudentSignUpView.as_view(), name='student_signup'),
]