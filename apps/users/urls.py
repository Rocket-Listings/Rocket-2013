from django.conf.urls import patterns, url, include
from registration.views import register

urlpatterns = patterns('',
	url(r'', include('registration.backends.simple.urls')),
    url(r'^$', 'users.views.overview'), # should replace with redirect to the user's profile url
    url(r'^(?P<username>\w+)$/', 'users.views.overview'),
    url(r'^info/$', 'users.views.info'), # this url makes registration redirect work
    url(r'^(?P<username>\w+)/info/$', 'users.views.info'),
    url(r'^(?P<username>\w+)/edit/$', 'users.views.edit'),
)