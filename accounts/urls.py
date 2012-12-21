from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login', 'accounts.views.login', name='login'),	
	url(r'^login-submit$', 'django.contrib.auth.views.login', name='login-submit'),
    url(r'^logout', 'accounts.views.logout', name='logout'),

)