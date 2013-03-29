from django.conf.urls import patterns, url
from listings.views import import_uploader

urlpatterns = patterns('listings.views',
	url(r'^$', 'latest'),
	url(r'^create/$', 'create'),
	url(r'^(?P<listing_id>\d+)/$', 'detail'),
	url(r'^(?P<listing_id>\d+)/messages/$', 'messages'),
	url(r'^(?P<listing_id>\d+)/offers/$', 'offers'),
	url(r'^(?P<listing_id>\d+)/cl-embed/$', 'embed'),	
	url(r'^(?P<listing_id>\d+)/update/$', 'update'),
	url(r'^(?P<listing_id>\d+)/delete/$', 'delete'),
	url(r'^(?P<listing_id>\d+)/delete_ajax/$', 'delete_ajax'),
	url(r'^ajax-photo-upload/$', import_uploader, name="ajax_photo_upload"),
	#api patterns
	url(r'^(?P<listing_id>\d+)/api/buyers/$', 'buyer_table'),
	url(r'^(?P<listing_id>\d+)/api/messages/(?P<buyer_id>\d+)/$', 'message_thread'),
)