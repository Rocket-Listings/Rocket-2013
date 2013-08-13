"""Heroku production settings and globals."""

from os import environ

from memcacheify import memcacheify
# from postgresify import postgresify
# from S3 import CallingFormat
# from boto.s3.connection import OrdinaryCallingFormat
import dj_database_url
from common import *

DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django_postgrespool'

DATABASE_POOL_ARGS = {
  'max_overflow': 10,
  'pool_size': 10,
  'recycle': 300
}

SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = memcacheify()

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
BROKER_TRANSPORT = 'amqplib'

# Set this number to the amount of allowed concurrent connections on your AMQP
# provider, divided by the amount of active workers you have.
#
# For example, if you have the 'Little Lemur' CloudAMQP plan (their free tier),
# they allow 3 concurrent connections. So if you run a single worker, you'd
# want this number to be 3. If you had 3 workers running, you'd lower this
# number to 1, since 3 workers each maintaining one open connection = 3
# connections total.
#
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-pool-limit
BROKER_POOL_LIMIT = 3

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-connection-max-retries
BROKER_CONNECTION_MAX_RETRIES = 0

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
BROKER_URL = environ.get('RABBITMQ_URL') or environ.get('CLOUDAMQP_URL')

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'amqp'

# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
)

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
# AWS_CALLING_FORMAT = OrdinaryCallingFormat
# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = environ.get('AWS_KEY', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')

AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIREY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate, no-transform' % (AWS_EXPIREY, AWS_EXPIREY)
}

S3_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = S3_STORAGE

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
# AWS_CALLING_FORMAT = OrdinaryCallingFormat
# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = environ.get('AWS_KEY', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')

AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIREY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate, no-transform' % (AWS_EXPIREY, AWS_EXPIREY)
}

STATIC_URL = S3_URL + 'assets/'
# COMPRESS_URL = 'http://static.rocketlistings.com.s3.amazonaws.com/assets/'

# COMPRESS_ROOT = STATIC_ROOT

COMPRESS_OFFLINE = True
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
STATICFILES_STORAGE = 'rocket.settings.storage.StaticCachedS3BotoStorage'
# COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
COMPRESS_STORAGE = 'rocket.settings.storage.CompressCachedS3BotoStorage'
COMPRESS_OUTPUT_DIR = 'compress'

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


# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
  '.herokuapp.com',
  'beta.rocketlistings.com' 
]

DOMAIN_NAME = "beta.rocketlistings.com"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}

############# MAILGUN CONFIG
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-9flqj538z-my-qcnpc74c2wit4vibl-3'
MAILGUN_SERVER_NAME = 'rocketlistings.mailgun.org'