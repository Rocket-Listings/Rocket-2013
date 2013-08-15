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

DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

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
BROKER_POOL_LIMIT = 1

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

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'rocket.settings.storage.NonPackagingS3PipelineStorage'

# STATIC_URL = S3_URL + 'assets/'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
# STATICFILES_STORAGE = 'rocket.settings.storage.ProductionStaticCachedS3BotoStorage'
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

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

AUTOPOST_DEBUG = False