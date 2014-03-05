from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    # Craigslist mail
	url(r'^test/$', 'mail.views.on_incoming_test_message'),
	url(r'^admin/$', 'mail.views.new_cl_admin_message'),
	url(r'^buyer/$', 'mail.views.new_cl_buyer_message'),

  url(r'^message/(?P<is_seller>\w+)/(?P<thread>\w+)$', 'mail.views.new_rocket_message'),
)
