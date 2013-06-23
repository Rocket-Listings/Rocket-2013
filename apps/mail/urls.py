from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^test/$', 'mail.views.on_incoming_test_message'),
	#url(r'^admin/$', ''),
)