from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# serving up static pages with RequestContext variables
urlpatterns = patterns('static_pages.views',
    url(r'^$', 'home', name='home'),
    url(r'^background/$', 'index', name='background'),
    url(r'^about/$', 'index', name='about'),
    url(r'^pricing/$', 'index', name='pricing'),
    # url(r'^help/$', 'help', name='help'),
    # url(r'^contact/$', 'contact', name='contact'),
    url(r'^/users/login/$', 'login', name='login'),
    url(r'^googlef43896b8ef9b394c.html', 'google_webmaster_verification'),
)