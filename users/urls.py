from django.conf.urls import patterns, url, include
from registration.views import register

urlpatterns = patterns('',
	url(r'^listings/$', 'users.views.listings'),
	url(r'^$', 'users.views.overview'),
    url(r'^(?P<username>\w+)$', 'users.views.overview'),
    url(r'^(?P<username>\w+)/listings$', 'users.views.listings'),
    url(r'^(?P<username>\w+)/info$', 'users.views.info'),
    url(r'^(?P<username>\w+)/edit$', 'users.views.edit'),
	(r'', include('registration.backends.simple.urls')),
)