from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    # Craigslist mail
	url(r'^test/$', 'mail.views.on_incoming_test_message'),
	url(r'^admin/$', 'mail.views.new_cl_admin_message'),
	url(r'^buyer/$', 'mail.views.new_cl_buyer_message'),

    url(r'^message/(?P<is_seller>\w+)/(?P<thread>\w+)$', 'mail.views.new_rocket_message'),
    # Send a message
    # url(r'^messages/send/(?P<message_id>\d+)$', 'mail.views.send_message'),

	url(r'^(?P<listing_id>\d+)/autopost/$', 'mail.views.autopost'),
)