from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^$', 'accounts.views.home', name='accounts_home'),   
	(r'', include('registration.backends.default.urls')),
)