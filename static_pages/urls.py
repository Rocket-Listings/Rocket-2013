from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

# serving up static pages with RequestContext variables
urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'home.html'}, name='home'),
	url(r'^help/$', direct_to_template, {'template':'help.html'}, name='help'),
	url(r'^contact/$', direct_to_template, {'template':'contact.html'}, name='contact'),
	url(r'^faq/$', direct_to_template, {'template':'faq.html'}, name='faq'),
	url(r'^about/$', direct_to_template, {'template':'about.html'}, name='about'),
)