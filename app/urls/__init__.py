"""
Url Patterns that the PersOA API uses
"""

from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^generate/', include('app.urls.generate')),
    url(r'^find/', 'app.views.find.find'),
    url(r'^', include('app.urls.index')),
)
