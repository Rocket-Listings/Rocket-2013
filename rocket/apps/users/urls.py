from django.conf.urls import patterns, url, include
from registration.views import register
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'', include('registration.backends.default.urls')),
    url(r'^info/$', 'users.views.info', name='user_info'), # this url makes registration redirect work
    url(r'^delete/$', 'users.views.delete_account', name='delete_account'),
    url(r'^twitter/$', 'users.views.obtain_twitter_auth_url', name='obtain_twitter_auth_url'),
    url(r'^twitter/callback/$', 'users.views.verify_twitter', name='verify_twitter'),
    url(r'^twitter/close/$', TemplateView.as_view(template_name='users/close.html')),
    url(r'^twitter/handle/$', 'users.views.get_twitter_handle', name='get_twitter_handle'),
    url(r'^twitter/disconnect/$', 'users.views.disconnect_twitter', name='disconnect_twitter'),
    url(r'^twitter/connected/$', 'users.views.twitter_connected', name='twitter_connected'),
    url(r'^twitter/oauth/$', 'users.views.have_oauth', name='have_oauth'),
    url(r'^(?P<username>\w+)/$', 'users.views.profile', name='user_profile'),
)