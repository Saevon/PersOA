from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Get data about personality details
    url(r'^details/', include('app.urls.details')),
    # generate choices for some traits
    url(r'^generate/', include('app.urls.generate')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # The admin parrt of the site
    url(r'^admin/', include(admin.site.urls)),
)
