from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from listings import api
from rest_framework.urlpatterns import format_suffix_patterns

from static_pages.views import http403, http404, http500

admin.autodiscover()

urlpatterns = patterns('',
	url(r'', include('static_pages.urls')),
	url(r'^mail/', include('mail.urls')),
	url(r'^listings/', include('listings.urls')),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^users/', include('users.urls')),
	url(r'^admin/', include(admin.site.urls)),

    # api patterns
    url(r'^api/listings$', api.ListingList.as_view()),
    url(r'^api/listings/(?P<pk>[0-9]+)$', api.ListingDetail.as_view()),
    url(r'^api/specs$', api.SpecList.as_view()),
    url(r'^api/specs/(?P<pk>[0-9]+)$', api.SpecDetail.as_view()),
    url(r'^api/photos$', api.ListingPhotoList.as_view()),
    url(r'^api/photos/(?P<pk>[0-9]+)$', api.ListingPhotoDetail.as_view()),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()

urlpatterns = format_suffix_patterns(urlpatterns)

handler403 = http403
handler404 = http404
handler500 = http500
