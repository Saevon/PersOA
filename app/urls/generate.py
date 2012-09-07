from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('app.views.generate',
    url(r'^generate/full', 'full'),
    url(r'^generate/group', 'group'),
    url(r'^generate/trait', 'trait'),
)
