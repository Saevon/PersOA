from django.conf.urls.defaults import patterns, url

# TODO: Add redirect to /index
urlpatterns = patterns('app.views.index',
    url(r'about', 'about'),
    url(r'index', 'index'),
)
