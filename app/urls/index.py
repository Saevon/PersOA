from django.conf.urls import url

from app.views import index

urlpatterns = [
    url(r'^$', index.index),
    url(r'^home', index.index),
    url(r'^index', index.index),
    url(r'^about', index.about),
]
