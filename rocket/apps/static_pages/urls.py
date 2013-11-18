from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from static_pages.views import index, google_webmaster_verification, home
# serving up static pages with RequestContext variables
urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^background/$', home, name='background'),
    url(r'^about/$', home, name='about'),
    # url(r'^pricing/$', 'index', name='pricing'),
    url(r'^googlef43896b8ef9b394c.html', google_webmaster_verification),
)