from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# serving up static pages with RequestContext variables
urlpatterns = patterns('static_pages.views',
    url(r'^$', 'home', name='home'),
    url(r'^background/$', 'homepage', name='background'),
    url(r'^about/$', 'homepage', name='about'),
    url(r'^pricing/$', 'homepage', name='pricing'),
    url(r'^help/$', 'help', name='help'),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^users/login/$', 'login', name='login'),
    url(r'^googlef43896b8ef9b394c.html', 'google_webmaster_verification'),
)