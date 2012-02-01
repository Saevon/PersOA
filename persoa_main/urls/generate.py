from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('persoa_main.views.generate',
    url(r'^full', 'full'),
    url(r'^group', 'group'),
    url(r'^trait', 'trait'),
)
