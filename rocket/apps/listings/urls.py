from django.conf.urls import patterns, url, include
# from listings.views import import_uploader

urlpatterns = patterns('listings.views',
	# url(r'^$', 'latest'),
	url(r'^create/$', 'create', {'pane':'edit'}, name='create'),
	url(r'^(?P<listing_id>\d+)/$', 'detail', {'pane': 'preview'}, name='detail'),
	url(r'^(?P<listing_id>\d+)/edit/$', 'detail', {'pane': 'edit' }, name='edit'),

	url(r'^search/$','search'),
	url(r'^search/ajax','search_ajax'),

	url(r'^(?P<listing_id>\d+)/delete/$', 'delete'),
	# url(r'^(?P<listing_id>\d+)/delete_ajax/$', 'delete_ajax'),

	url(r'^(?P<listing_id>\d+)/cl-embed/$', 'embed'),
	# url(r'^ajax-photo-upload/$', import_uploader, name="ajax_photo_upload"),

	url(r'^dashboard/$', 'dashboard', name='dashboard'),

	url(r'^dashboard/data/$','dashboard_data'),
	url(r'^dashboard/message/$', 'dashboard_message'),
	url(r'^dashboard/message/seen/$', 'message_seen'),
	url(r'^(?P<listing_id>\d+)/status/$', 'status'),
)