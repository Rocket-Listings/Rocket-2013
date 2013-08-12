from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# serving up static pages with RequestContext variables
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='static_pages/what.html'), name='home'),
    url(r'^what/$', TemplateView.as_view(template_name='static_pages/what.html'), name='what'),
    url(r'^how/$', TemplateView.as_view(template_name='static_pages/how.html'), name='how'),
    url(r'^why/$', TemplateView.as_view(template_name='static_pages/why.html'), name='why'),
    url(r'^pricing/$', TemplateView.as_view(template_name='static_pages/pricing.html'), name='pricing'),

	url(r'^help/$', TemplateView.as_view(template_name='static_pages/help.html'), name='help'),
	url(r'^contact/$', TemplateView.as_view(template_name='static_pages/contact.html'), name='contact'),
	url(r'^faq/$', TemplateView.as_view(template_name='static_pages/faq.html'), name='faq'),
	
    url(r'^/users/login/$', TemplateView.as_view(template_name='rocket_registration/login.html'), name='login'),
)