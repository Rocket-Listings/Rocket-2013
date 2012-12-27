from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^listings/', include('listings.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
   	url(r'^accounts/', include('accounts.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'', include('static_pages.urls')),
)