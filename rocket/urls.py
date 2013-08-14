from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from static_pages.views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'', include('static_pages.urls')),
	url(r'^mail/', include('mail.urls')),
	url(r'^listings/', include('listings.urls')),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^users/', include('users.urls')),
	url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()

handler403 = http403
handler404 = http404
handler500 = http500