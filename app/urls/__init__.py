"""
Url Patterns that the PersOA API uses
"""

from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^generate/', include('app.urls.generate')),
    url(r'^find/', include('app.urls.find')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('app.urls.index')),
)
