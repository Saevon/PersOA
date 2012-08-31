"""
Url Patterns that the PersOA API uses
"""

from django.conf.urls.defaults import patterns, url

from app.urls import details, generate, index

urlpatterns = []
# perhaps use app.urls? and import all sub modules?
for module in [details, generate, index]:
	urlpatterns += module.urlpatterns
