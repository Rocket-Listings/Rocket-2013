import sys
from os.path import join, abspath, dirname

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SITE_ID = 1

ROOT_URLCONF = 'rocketlistings.urls'
WSGI_APPLICATION = 'settings.wsgi.application'

SITE_ROOT = dirname(dirname(abspath(__file__)))
sys.path.append(SITE_ROOT)
sys.path.append(join(SITE_ROOT, 'apps'))

SECRET_KEY = '59%5@qdw12&amp;d)47=3=$ar4bv4vcgk)*-_f2=qr9(n9jy%z%1j!'

MANAGERS = ADMINS = (
	 ('Teddy Knox', 'teddy@rocketlistings.com'),
	 ('Brian Sirkia', 'brian@rocketlistings.com'),
	 ('Nat Kelner', 'nat@rocketlistings.com'),
)

AUTH_PROFILE_MODULE = 'users.UserProfile'

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL = '/users/login/' # references users/urls.py name
LOGOUT_URL = '/users/logout/' #references users/urls.py name
LOGIN_REDIRECT_URL = '/users/info/'
LOGOUT_REDIRECT_URL = '/'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
DATE_FORMAT = ('%m/%d/%y %H:%M',)

USE_I18N = False
USE_L10N = True
USE_TZ = True


STATIC_ROOT = join(SITE_ROOT, 'static_collected/')

# Minimum time that uploaded photos will stay on server if not assigned to a listing.
ROCKET_UNUSED_PHOTO_MINS = 10

SOUTH_AUTO_FREEZE_APP = True

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-9flqj538z-my-qcnpc74c2wit4vibl-3'
MAILGUN_SERVER_NAME = 'rocketlistings.mailgun.org'

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
	'compressor.finders.CompressorFinder',
)

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
	'django.core.context_processors.csrf',
	'django.contrib.auth.context_processors.auth',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request', # suit installation
)

MIDDLEWARE_CLASSES = (
	'django.middleware.cache.UpdateCacheMiddleware',
	'django.middleware.gzip.GZipMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
		#'django.middleware.cache.FetchFromCacheMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'pagination.middleware.PaginationMiddleware',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'haystack',
	'south',
	'registration',
	'ajaxuploader',
	'sorl.thumbnail',
	'storages',
	'pagination',
	'compressor',

	# our apps
	'rocketlistings',
	'static_pages',
	'listings',
	'users',
	'mail',
)

HAYSTACK_CONNECTIONS = {
		'default': {
				'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
				'PATH': join(abspath(__file__), 'whoosh_index'),
		}
}

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
