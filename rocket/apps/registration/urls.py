from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from registration.views import activate
from registration.views import register
from static_pages.views import index

urlpatterns = patterns('',
    (r'', include('registration.auth_urls')),
    url(r'^activate/(?P<activation_key>\w+)/$', activate, name='registration_activate'),
    url(r'^register/$', register, name='register'),
    url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
    url(r'^register/closed/$', TemplateView.as_view(template_name='registration/registration_closed.html'), name='registration_disallowed'),
)
