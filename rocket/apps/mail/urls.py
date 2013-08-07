from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    # Craigslist mail
	url(r'^test/$', 'mail.views.on_incoming_test_message'),
	url(r'^admin/$', 'mail.views.on_incoming_admin_message'),
	url(r'^buyer/$', 'mail.views.on_incoming_buyer_message'),

    # Redirected mail from sellers/buyers
    url(r'^tobuyer/$', 'mail.views.new_message_to_buyer'),
    url(r'^toseller/$', 'mail.views.new_message_to_seller'),

    # Send a message
    # url(r'^messages/send/(?P<message_id>\d+)$', 'mail.views.send_message'),

	url(r'^(?P<listing_id>\d+)/autopost/$', 'mail.views.autopost'),
)