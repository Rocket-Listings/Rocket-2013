from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
	url(r'^login', 'login', name='login'),	
    url(r'^$', 'home', name='account-home'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^login-action$', 'login', name='login-action'),
    url(r'^logout', 'logout', name='logout'),
)