import re
from django.test import TestCase, Client
from django.core import mail
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading


NO_SETTING = ('!', None)

class TestSettingsManager(object):
    """
    A class which can modify some Django settings temporarily for a
    test and then revert them to their original values later.

    Automatically handles resyncing the DB if INSTALLED_APPS is
    modified.

    """
    def __init__(self):
        self._original_settings = {}

    def set(self, **kwargs):
        for k,v in kwargs.iteritems():
            self._original_settings.setdefault(k, getattr(settings, k,
                                                          NO_SETTING))
            setattr(settings, k, v)
        if 'INSTALLED_APPS' in kwargs:
            self.syncdb()

    def syncdb(self):
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)

    def revert(self):
        for k,v in self._original_settings.iteritems():
            if v == NO_SETTING:
                delattr(settings, k)
            else:
                setattr(settings, k, v)
        if 'INSTALLED_APPS' in self._original_settings:
            self.syncdb()
        self._original_settings = {}


class SettingsTestCase(TestCase):
    """
    A subclass of the Django TestCase with a settings_manager
    attribute which is an instance of TestSettingsManager.

    Comes with a tearDown() method that calls
    self.settings_manager.revert().

    """
    def __init__(self, *args, **kwargs):
        super(SettingsTestCase, self).__init__(*args, **kwargs)
        self.settings_manager = TestSettingsManager()
    
    def tearDown(self):
        self.settings_manager.revert()

class UserTest(SettingsTestCase):

    def __init__(self, *args, **kwargs):
        super(UserTest, self).__init__(*args, **kwargs)

    def setUp(self):
        self.settings_manager.set(
            STATICFILES_STORAGE='pipeline.storage.NonPackagingPipelineStorage')


    def test_email_activation(self):
        """
        Tests that email activation is working
        """

        c = Client()
        response = c.post('/users/register/', {'username':'test', 'email':'test@test.com', 'password1':'test', 'password2':'test'}, follow = True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response, '/users/register/complete/')
        activation_email = mail.outbox[0].body
        activation_path = re.findall(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', str(activation_email))[0].split('8000')[1]
        response = c.get('activation_path', follow =True)
        self.assertEqual(response.status_code, 200)
        


        
