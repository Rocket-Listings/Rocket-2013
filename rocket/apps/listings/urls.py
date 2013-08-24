from django.conf.urls import patterns, url, include

urlpatterns = patterns('listings.views',
    url(r'^new/$', 'create', name='create'),   
    # the next two point to the same view
    url(r'^(?P<listing_id>\d+)/$', 'detail', {'pane': 'preview'}, name='detail'),
    url(r'^(?P<listing_id>\d+)/edit/$', 'detail', {'pane': 'edit' }, name='edit'),
    url(r'^search/$','search'),
    # url(r'^(?P<listing_id>\d+)/cl-embed/$', 'embed'),
    url(r'^(?P<listing_id>\d+)/autopost/$', 'autopost', name='autopost'),
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
)

urlpatterns += patterns('listings.api',
    url(r'^search/ajax','search_ajax'),
    url(r'^dashboard/data/$','dashboard_data'),
    url(r'^dashboard/message/$', 'dashboard_message'),
    url(r'^dashboard/message/seen/$', 'message_seen'),
    url(r'^(?P<listing_id>\d+)/status/$', 'status'),
    url(r'^(?P<listing_id>\d+)/status/update/$', 'update_status'),
    url(r'^(?P<listing_id>\d+)/delete/$', 'delete'),
)