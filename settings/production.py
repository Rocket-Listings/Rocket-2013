from common import *
import dj_database_url, os

# Debug Settings
DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

# Http Settings
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
PREPEND_WWW = False

DOMAIN_NAME = "beta.rocketlistings.com"
SITE_NAME = "Rocket"
ALLOWED_HOSTS = [   'beta.rocketlistings.com',
                    'rocket-listings.herokuapp.com' ]


# Database settings sourced from Heroku
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django_postgrespool'
DATABASE_POOL_ARGS = {
    'max_overflow': 10,
    'pool_size': 10,
    'recycle': 300
}
SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}

# S3 settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET')

# see http://developer.yahoo.com/performance/rules.html#expires
AWS_HEADERS = {
    'Cache-Control': 'max-age=86400, pubic',
}

DEFAULT_FILE_STORAGE = "settings.storage.S3MediaStorage"
STATICFILES_STORAGE = "settings.storage.CachedS3StaticStorage"
COMPRESS_STORAGE = "settings.storage.CachedS3StaticStorage"

UPLOAD_DIR = 'uploads'

STATIC_URL = "https://{0}.s3.amazonaws.com/static/".format(AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = "https://{0}.s3.amazonaws.com/media/".format(AWS_STORAGE_BUCKET_NAME)
#AWS_S3_CUSTOM_DOMAIN = "s3.amazonaws.com/media.rocketlistings.com"
AWS_S3_SECURE_URLS = False

COMPRESS_OFFLINE = True

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
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
