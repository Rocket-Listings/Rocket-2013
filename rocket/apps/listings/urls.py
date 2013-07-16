from django.conf.urls import patterns, url, include
# from listings.views import import_uploader

urlpatterns = patterns('listings.views',
	url(r'^search/$','search'),
	url(r'^search/ajax/$','search_listings'),
	#url(r'^$', 'latest'),
	url(r'^create/$', 'create'),
	url(r'^(?P<listing_id>\d+)/$', 'detail'),
	url(r'^(?P<listing_id>\d+)/update/$', 'update'),
	url(r'^(?P<listing_id>\d+)/delete/$', 'delete'),
	# url(r'^(?P<listing_id>\d+)/delete_ajax/$', 'delete_ajax'),

	url(r'^(?P<listing_id>\d+)/cl-embed/$', 'embed'),
	# url(r'^ajax-photo-upload/$', import_uploader, name="ajax_photo_upload"),

	url(r'^dashboard/$', 'dashboard', name='dashboard'),
  url(r'^(?P<username>\w+)/$', 'user_listings', name='user_listings'),

	#api patterns TODO: respond differently based on HTTP_ACCEPT header, but keep urls the same
	url(r'^(?P<listing_id>\d+)/api/buyers/$', 'listing_buyers_ajax'),
	url(r'^(?P<listing_id>\d+)/api/messages/(?P<buyer_id>\d+)/$', 'message_thread_ajax'),
)