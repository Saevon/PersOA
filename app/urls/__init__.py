"""
Url Patterns that the PersOA API uses
"""

from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

from app.views import find

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^generate/', include('app.urls.generate')),
    url(r'^find/', find),
    url(r'^', include('app.urls.index')),
]
