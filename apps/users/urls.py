from django.conf.urls import patterns, url, include
from registration.views import register


urlpatterns = patterns('',
    url(r'', include('registration.backends.simple.urls')),
    url(r'^info/$', 'users.views.info'), # this url makes registration redirect work
    # url(r'^(?P<username>\w+)/info/$', 'users.views.info', name='user_info'),
    url(r'^(?P<username>\w+)/$', 'users.views.profile'),
)