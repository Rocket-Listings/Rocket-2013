"""Settings and globals for both development and production."""

from datetime import timedelta
from sys import path
from os.path import abspath, basename, dirname, join, normpath
from djcelery import setup_loader
from os import environ


# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
path.append(join(DJANGO_ROOT, 'apps'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG

THUMBNAIL_DEBUG = DEBUG

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS = (
	('Teddy Knox', 'teddy@rocketlistings.com'),
	('Brian Sirkia', 'brian@rocketlistings.com'),
	('Nat Kelner', 'nat@rocketlistings.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
  }
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'America/New_York'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'static_collected'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
  normpath(join(DJANGO_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  'compressor.finders.CompressorFinder',
)

AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', 'static.rocketlistings.com')

S3_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = '59%5@qdw12&amp;d)47=3=$ar4bv4vcgk)*-_f2=qr9(n9jy%z%1j!'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
  normpath(join(DJANGO_ROOT, 'fixtures')),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  'django.core.context_processors.tz',
  'django.contrib.messages.context_processors.messages',
  'django.core.context_processors.request',
  "listings.context_processors.s3_url",
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
  normpath(join(DJANGO_ROOT, 'templates')),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
  # Use GZip compression to reduce bandwidth.
  'django.middleware.gzip.GZipMiddleware',

  # Default Django middleware.
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME

DJANGO_APPS = (
  # Default Django apps:
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  # Useful template tags:
  'django.contrib.humanize',

  # Admin panel and documentation:
  'django.contrib.admin',
  'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
  # Database migration helpers:
  'south',

  # Static file management:
  'compressor',

  # Asynchronous task queue:
  'djcelery',

  # search
	'haystack',

	# thumbnails
	'sorl.thumbnail',

	# pagination template tags
	'pagination',

	# static file management
	'compressor',


)

LOCAL_APPS = (
	'listings',
	'mail',
	'registration',
	'static_pages',
	'users',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
  'require_debug_false': {
    '()': 'django.utils.log.RequireDebugFalse'
    }
  },
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
      'filters': ['require_debug_false'],
      'class': 'django.utils.log.AdminEmailHandler'
    },
    'console': {
      'level': 'DEBUG',
      'class': 'logging.StreamHandler'
    }
  },
  'loggers': {
    'django.request': {
      'handlers': ['mail_admins', 'console'],
      'level': 'ERROR',
      'propagate': True,
    },
  }
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'


############# CELERY CONFIG
# See: http://celery.readthedocs.org/en/latest/configuration.html#celery-task-result-expires
CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)

# See: http://celery.github.com/celery/django/
setup_loader()


############# COMPRESS CONFIG
# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_PRECOMPILERS
COMPRESS_PRECOMPILERS = (
  ('text/less', 'lessc {infile} {outfile}'),
)

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_CSS_FILTERS
COMPRESS_CSS_FILTERS = [
  'compressor.filters.css_default.CssAbsoluteFilter',
  'compressor.filters.template.TemplateFilter',
  'compressor.filters.cssmin.CSSMinFilter',
]

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_JS_FILTERS
COMPRESS_JS_FILTERS = [
  # 'compressor.filters.template.TemplateFilter',
  'compressor.filters.jsmin.JSMinFilter',
]

############# USER ACCOUNTS CONFIG
AUTH_PROFILE_MODULE = 'users.UserProfile'

ACCOUNT_ACTIVATION_DAYS = 7

DEFAULT_FROM_EMAIL = 'webmaster@localhost:8000'

LOGIN_URL = '/users/login/' # references users/urls.py name

LOGOUT_URL = '/users/logout/' #references users/urls.py name

LOGIN_REDIRECT_URL = '/users/info/'

LOGOUT_REDIRECT_URL = '/'

# Minimum time that uploaded photos will stay on server if not assigned to a listing.
ROCKET_UNUSED_PHOTO_MINS = 10

# HAYSTACK CONFIG
HAYSTACK_CONNECTIONS = {
		'default': {
				'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
				'PATH': join(dirname(__file__), 'whoosh_index'),
		}
}