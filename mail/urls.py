from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^$', 'mail.views.on_incoming_message'),
)