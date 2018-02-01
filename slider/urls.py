#slider/urls
# main url controller
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Auth
    url(r'^accounts/', include('django.contrib.auth.urls')),
    # connect carousel app
    url(r'^', include('carousel.urls')),
    # connect comments app
    url(r'^comments/', include('comments.urls')), 
    # connect User Management app
    url(r'^', include('user_management.urls')), 
    ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
