from django.conf.urls.defaults import patterns, url

# TODO: Add redirect to /index
urlpatterns = patterns('app.views.index',
	url(r'', 'index'),
	url(r'home', 'index'),
    url(r'index', 'index'),
    url(r'about', 'about'),
)
