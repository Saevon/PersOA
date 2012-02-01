from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('persoa_main.views.details',
    url(r'^choices', 'choices'),
    url(r'^traits', 'traits'),
    url(r'^trait_groups', 'trait_groups'),
)
