from django.conf.urls import patterns, url

# for django 1.4.x support
def template_view(template_name):
    try:
        from django.views.generic.simple import direct_to_template
        def curried_template_view(request, extra_context=None, mimetype=None, **kwargs):
            return direct_to_template(request, template_name, extra_context, mimetype, **kwargs)
        return curried_template_view
    except ImportError:
        from django.views.generic import TemplateView
        return TemplateView.as_view(template_name=template_name)

# serving up static pages with RequestContext variables
urlpatterns = patterns('',
    url(r'^$', template_view('home.html'), name='home'),
	url(r'^help/$', template_view('help.html'), name='help'),
	url(r'^contact/$', template_view('contact.html'), name='contact'),
	url(r'^faq/$', template_view('faq.html'), name='faq'),
	url(r'^about/$', template_view('about.html'), name='about'),
)