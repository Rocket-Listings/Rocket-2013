from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^$', 'accounts.views.overview'),
    url(r'^(?P<username>\w+)/$', 'accounts.views.overview'),
    url(r'^(?P<username>\w+)/listings/$', 'accounts.views.listings'),
    url(r'^(?P<username>\w+)/info/$', 'accounts.views.info'),
	(r'', include('registration.backends.default.urls')),
)