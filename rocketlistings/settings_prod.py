import dj_database_url,os

DB =  dj_database_url.config()

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

AWS_ACCESS_KEY_ID = os.environ.get('AWS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET')
AWS_STORAGE_BUCKET_NAME = 'static.rocketlistings.com'

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://static.rocketlistings.com/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.comhttp://static.rocketlistings.com/"
STATIC_URL = 'http://static.rocketlistings.com/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

PREPEND_WWW = False

# os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
# os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
# os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

# if bool(os.environ.get('LOCAL_MEMCACHE', '')):
#     CACHES = {
#       'default': {
#         'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#         'LOCATION': os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';'),
#         'TIMEOUT': 500,
#         'BINARY': True,
#       }
#     }

# ##CACHE_MIDDLEWARE_ALIAS = 'local-rocket-cache'
# ##CACHE_MIDDLEWARE_SECONDS = 300
# ##CACHE_MIDDLEWARE_KEY_PREFIX = 'rocketlistings'
# CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True # Caching only anonymous pages.

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