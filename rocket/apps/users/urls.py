from django.conf.urls import patterns, url, include
from registration.views import register


urlpatterns = patterns('',
    url(r'', include('registration.backends.default.urls')),
    url(r'^info/$', 'users.views.info', name='user_info'), # this url makes registration redirect work
    url(r'^delete/$', 'users.views.delete_account', name='delete_account'),
    url(r'^(?P<username>\w+)/$', 'users.views.profile', name='user_profile'),
)