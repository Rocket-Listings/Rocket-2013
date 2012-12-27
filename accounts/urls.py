from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^(?P<username>\w+)$', 'accounts.views.overview', name='account_overview'),
	url(r'^$', 'accounts.views.overview', name='account_overview'),
    url(r'^(?P<username>\w+)/listings$', 'accounts.views.listings', name='account_listings'),
    url(r'^(?P<username>\w+)/info$', 'accounts.views.info', name='account_info'),
	(r'', include('registration.backends.default.urls')),
)