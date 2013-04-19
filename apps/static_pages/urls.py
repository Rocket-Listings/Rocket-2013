from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# serving up static pages with RequestContext variables
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
	url(r'^help/$', TemplateView.as_view(template_name='help.html'), name='help'),
	url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
	url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name='faq'),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
	url(r'^features/$', TemplateView.as_view(template_name='features.html'), name='features'),
)