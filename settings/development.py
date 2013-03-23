from common import *
from path import path

# General settings
DEBUG = True
PREPEND_WWW = False
PRODUCTION = False

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Database settings
DATABASES = { 
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2' , # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'rocket',                      # Or path to database file if using sqlite3.
		'USER': 'teddyknox',                      # Not used with sqlite3.
		'PASSWORD': '',                  # Not used with sqlite3.
		'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
	}
}

# file storage settings
STATIC_ROOT = SITE_ROOT / 'static_collected/'
MEDIA_ROOT =  SITE_ROOT / 'media/'
UPLOAD_DIR = 'uploads'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
UPLOAD_URL = MEDIA_URL + 'uploads/'

# Logging settings
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
	},
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'console':{
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers':['console'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}