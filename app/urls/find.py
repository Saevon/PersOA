from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('app.views.find',
    url(r'^choice', 'choice', {'single': True}),
    url(r'^choices', 'choice', {'single': False}),
    url(r'^trait', 'trait'),
    url(r'^traits', 'traits'),
    url(r'^group', 'trait_group', {'single': True}),
    url(r'^groups', 'trait_group', {'single': False}),
)
