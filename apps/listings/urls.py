from django.conf.urls import patterns, url
from listings.views import import_uploader

urlpatterns = patterns('listings.views',
	url(r'^$', 'latest'),
	url(r'^category/$', 'category'),
	url(r'^(?P<listing_id>\d+)/$', 'detail'),
	url(r'^(?P<listing_id>\d+)/messages/$', 'messages'),
	url(r'^(?P<listing_id>\d+)/offers/$', 'offers'),
	url(r'^(?P<listing_id>\d+)/autopost/$', 'autopost'),
	url(r'^(?P<listing_id>\d+)/cl-embed/$', 'embed'),	
	url(r'^(?P<listing_id>\d+)/update/$', 'update'),
	url(r'^(?P<listing_id>\d+)/delete/$', 'delete'),
	url(r'^(?P<listing_id>\d+)/delete_ajax/$', 'delete_ajax'),
	url(r'^ajax-photo-upload/$', import_uploader, name="ajax_photo_upload"),

	# moved here from users/urls.py
    url(r'^(?P<username>\w+)/dashboard/$', 'dashboard'),
    url(r'^(?P<username>\w+)/$', 'user_listings', name='user_listings'),

	#api patterns TODO: respond differently based on HTTP_ACCEPT header, but keep urls the same
	url(r'^(?P<listing_id>\d+)/api/buyers/$', 'ajax_listing_buyers'),
	url(r'^(?P<listing_id>\d+)/api/messages/(?P<buyer_id>\d+)/$', 'ajax_message_thread'),
)