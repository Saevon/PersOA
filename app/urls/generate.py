from django.conf.urls import url

from app.views import generate

urlpatterns = [
    url(r'^profile', generate.profile),
    url(r'^group', generate.group),
    url(r'^trait', generate.trait),
]
