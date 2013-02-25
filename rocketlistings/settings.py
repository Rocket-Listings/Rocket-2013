# Django settings for rocketlistings project.
import os

 # DATABASE_URL is a heroku env var
if bool(os.environ.get('DATABASE_URL', '')):
    from settings_prod import *
else:
    from settings_dev import *

DATABASES = { 'default': DB }
    
#APP_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'users.UserProfile'
ADMINS = (
     ('Teddy Knox', 'teddy@rocketlistings.com'),
     ('Brian Sirkia', 'brian@rocketlistings.com'),
     ('Nat Kelner', 'nat@rocketlistings.com'),
)

LOGIN_URL = '/users/login/' # references users/urls.py name
LOGOUT_URL = '/users/logout/' #references users/urls.py name
LOGIN_REDIRECT_URL = '/users/'
LOGOUT_REDIRECT_URL = '/'

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = SITE_ROOT+'/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')
STATIC_ROOT = SITE_ROOT+'/static_collected/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Minimum time that uploaded photos will stay on server if not assigned to a listing.
ROCKET_UNUSED_PHOTO_MINS = 10
SOUTH_AUTO_FREEZE_APP = True
# need this so that users is used instead of user
#ABSOLUTE_URL_OVERRIDES = {
#    'auth.user': lambda u: "/users/%s" % u.username,
#}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '59%5@qdw12&amp;d)47=3=$ar4bv4vcgk)*-_f2=qr9(n9jy%z%1j!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rocketlistings.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rocketlistings.wsgi.application'

TEMPLATE_DIRS = (
    #'/templates/',
    #os.path.join(SITE_ROOT, 'templates'),
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
#    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'suit',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'haystack',
    'rocketlistings',
    'static_pages',
    'listings',
    'users',
    'south',
    'registration',
    'ajaxuploader',
    'sorl.thumbnail',
    'django_extensions', #added for some extra tools like reset_db
    'storages',
)

HAYSTACK_SITECONF = 'rocketlistings.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(os.path.dirname(__file__), 'whoosh_index')

ACCOUNT_ACTIVATION_DAYS = 7