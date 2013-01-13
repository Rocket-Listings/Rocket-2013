from django.conf.urls import patterns, url
from listings.views import *

urlpatterns = patterns('listings.views',
	url(r'^$', latest),
	url(r'^create/$', create),
	url(r'^(?P<listing_id>\d+)/$', detail),
	url(r'^(?P<listing_id>\d+)/update/$', update),
	url(r'^(?P<listing_id>\d+)/delete/$', delete),
	url(r'^ajax-photo-upload/$', import_uploader, name="ajax_photo_upload"),
)