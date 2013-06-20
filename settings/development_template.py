from common import *
from os.path import join

# General settings
DEBUG = True
PREPEND_WWW = False
PRODUCTION = False

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Database settings
SOUTH_DATABASE_ADAPTERS = {'default':'south.db.postgresql_psycopg2'}
DATABASES = { 
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2' ,
		'NAME': '', # Defaults to your computer username
		'USER': '', # Defaults to your computer username
		'PASSWORD': '', # Leave this blank by default
		'HOST': 'localhost',
		'PORT': '',
	}
}


# file storage settings
STATIC_ROOT = join(SITE_ROOT, 'static_collected/')
MEDIA_ROOT =  join(SITE_ROOT, 'media/')
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
			'handlers': ['console'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}