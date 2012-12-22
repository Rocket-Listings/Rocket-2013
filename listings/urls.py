from django.conf.urls import patterns, url
#from listings.views import latest, create

urlpatterns = patterns('listings.views',
    url(r'^$', 'latest', name='latest-listings'),
    url(r'^(?P<listing_id>\d+)$', 'read'),
    url(r'^create$', 'create'),
#    url(r'^(?P<listing_id>\d+)/update$', 'update'),
#    url(r'^(?P<listing_id>\d+)/delete$', 'delete'),
)