from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# serving up static pages with RequestContext variables
urlpatterns = patterns('static_pages.views',
    url(r'^$', 'home', name='home'),
    url(r'^what/$', 'homepage', name='what'),
    url(r'^how/$', 'homepage', name='how'),
    url(r'^why/$', 'homepage', name='why'),
    url(r'^pricing/$', 'homepage', name='pricing'),

	url(r'^help/$', 'help', name='help'),
	url(r'^contact/$', 'contact', name='contact'),
	url(r'^faq/$', 'faq', name='faq'),
    url(r'^/users/login/$', 'login', name='login'),
)