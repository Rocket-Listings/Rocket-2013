import dj_database_url,os

# General Settings
DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
PREPEND_WWW = False

# Database settings sourced from Heroku
DB =  dj_database_url.config()

# File storage settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET')
# AWS_STORAGE_BUCKET_NAME = 'static.rocketlistings.com'

STATICFILES_STORAGE = 'rocketlistings.s3storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'rocketlistings.s3storages.MediaStorage'

UPLOAD_DIR = 'uploads'

# not using static.rocketlistings.com because its CNAME 
# redirects to 'static.rocketlistings.com.s3-website-us-east-1.amazonaws.com' 
# and that doesn't work with SSL apparently because of the '.' char.
STATIC_URL = '//s3.amazonaws.com/static.rocketlistings.com/'
MEDIA_URL = '//s3.amazonaws.com/media.rocketlistings.com/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Caching settings
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

if bool(os.environ.get('LOCAL_MEMCACHE', '')):
    CACHES = {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';'),
        'TIMEOUT': 500,
        'BINARY': True,
      }
    }

##CACHE_MIDDLEWARE_ALIAS = 'local-rocket-cache'
##CACHE_MIDDLEWARE_SECONDS = 300
##CACHE_MIDDLEWARE_KEY_PREFIX = 'rocketlistings'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True # Caching only anonymous pages.

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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}