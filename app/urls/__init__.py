"""
Url Patterns that the PersOA API uses
"""

from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
admin.autodiscover()

from app.urls import details, generate, index

urlpatterns = []
# perhaps use app.urls? and import all sub modules?
for module in [details, generate, index]:
	urlpatterns += module.urlpatterns

urlpatterns += url(r'^admin/', include(admin.site.urls)),