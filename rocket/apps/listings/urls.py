from django.conf.urls import patterns, url, include
from listings import api
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('listings.views',
    url(r'^new/$', 'create', name='create'),
    
    # the next two point to the same view
    url(r'^(?P<listing_id>\d+)/$', 'detail', {'pane': 'preview'}, name='detail'),
    url(r'^(?P<listing_id>\d+)/edit/$', 'detail', {'pane': 'edit' }, name='edit'),

    url(r'^search/$','search'),
    # url(r'^(?P<listing_id>\d+)/cl-embed/$', 'embed'),
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

    url(r'^api/$', api.ListingList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', api.ListingDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)