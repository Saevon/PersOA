"""
Url Patterns that the PersOA API uses
"""

from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
admin.autodiscover()

from app.urls import index

urlpatterns = patterns('',
    url(r'^generate', include('app.urls.generate')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('app.urls.index')),
)
