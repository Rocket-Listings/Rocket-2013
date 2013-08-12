"""Local staging settings and globals."""

from os import environ
from common import *

SITE_ID = 1

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": environ.get('POSTGRES_DB_NAME', environ.get('USER', '')),
        "USER": environ.get('POSTGRES_USER_NAME', environ.get('USER', '')),
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = environ.get('AWS_KEY', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
# AWS_CALLING_FORMAT = OrdinaryCallingFormat
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIREY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate, no-transform' % (AWS_EXPIREY, AWS_EXPIREY)
}

S3_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_CACHED_STORAGE = 'rocket.settings.storage.LocalCachedS3BotoStorage'

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
DEFAULT_FILE_STORAGE = S3_STORAGE

STATICFILES_STORAGE = S3_CACHED_STORAGE

STATIC_URL = S3_URL # S3_URL defined in common.py

INSTALLED_APPS += (
    'storages',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = S3_URL # S3_URL defined in common.py

# CELERY CONFIG

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
# BROKER_TRANSPORT = 'amqplib'

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
# BROKER_URL = environ.get('RABBITMQ_URL') or environ.get('CLOUDAMQP_URL')

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'amqp'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*'] 

# DOMAIN_NAME = "beta.rocketlistings.com"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}

############# MAILGUN CONFIG
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-9flqj538z-my-qcnpc74c2wit4vibl-3'
MAILGUN_SERVER_NAME = 'rocketlistings.mailgun.org'