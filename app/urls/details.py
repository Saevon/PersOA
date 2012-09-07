from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('app.views.details',
    url(r'^details/choices', 'choices'),
    url(r'^details/traits', 'traits'),
    url(r'^details/trait_groups', 'trait_groups'),
)
