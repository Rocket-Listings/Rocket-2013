from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^listings/', include('listings.urls')),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^users/', include('users.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'', include('static_pages.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)