from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^test/$', 'mail.views.on_incoming_test_message'),
	url(r'^admin/$', 'mail.views.on_incoming_admin_message'),
	url(r'^buyer/$', 'mail.views.on_incoming_buyer_message')
)