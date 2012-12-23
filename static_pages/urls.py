from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^help$', 'static_pages.views.help', name='help'),
	url(r'^contact$', 'static_pages.views.contact', name='contact'),
	url(r'^faq$', 'static_pages.views.faq', name='faq'),
	url(r'^about$', 'static_pages.views.about', name='about'),
)