#from fabric_heroku_postgresql.core import *
from fabric.api import local, env, require

def resetdb():
  local('rm -f rocket/default.db')
  local('python manage.py syncdb --noinput --migrate')
  local('python manage.py loaddata messages_demo.yaml')
  local('python manage.py rebuild_index --noinput')

def deploy():
    """fab [environment] deploy"""

    # require('AWS_KEY')
    # require('AWS_SECRET')
    # require('AWS_STORAGE_BUCKET_NAME')
    # require('HEROKU_APP')

    local('heroku maintenance:on')
    local('DJANGO_SETTINGS_MODULE=rocket.settings.staging python manage.py collectstatic --noinput')
    local('git push heroku HEAD:master')
    local('heroku run python manage.py syncdb --noinput')
    local('heroku run python manage.py migrate')
    local('heroku run python manage.py collectstatic --noinput')
    local('heroku maintenance:off')
    local('heroku ps')
    local('heroku open')

def deploy_staging():
  local('heroku maintenance:on --app rocket-listings-staging')
  local('DJANGO_SETTINGS_MODULE=rocket.settings.staging python manage.py collectstatic --noinput')
  local('git push staging HEAD:master')
  local('heroku run python manage.py syncdb --noinput --app rocket-listings-staging')
  local('heroku run python manage.py migrate --app rocket-listings-staging')
  local('heroku run python manage.py collectstatic --noinput --app rocket-listings-staging')
  local('heroku maintenance:off --app rocket-listings-staging')
  local('heroku ps --app rocket-listings-staging')
  local('heroku open --app rocket-listings-staging')

<<<<<<< HEAD
=======
# def config():
#   # local('heroku config:set AWS_KEY=AKIAJDDGALJ4HWXOJM2A --app rocket-listings-staging')
#   # local('heroku config:set AWS_SECRET=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 --app rocket-listings-staging')
#   # local('heroku config:set AWS_STORAGE_BUCKET_NAME=static.rocketlistings.com --app rocket-listings-staging')
#   # local('heroku config:set BUILDPACK_URL=git://github.com/heroku/heroku-buildpack-python.git --app rocket-listings-staging')
#   # local('heroku config:set DISABLE_INJECTION=true --app rocket-listings-staging')
#   # local('heroku config:set DJANGO_SETTINGS_MODULE=rocket.settings.production --app rocket-listings-staging')
#   # local('heroku config:set PYTHONPATH=fakepath --app rocket-listings-staging')
#   # local('heroku config:set SECRET_KEY=59%5@qdw12&amp;d)47=3=$ar4bv4vcgk)*-_f2=qr9(n9jy%z%1j! --app rocket-listings-staging')
#   local('heroku config:set TWITTER_KEY=bZMfei7vpcVLbGJa2IdXw --app rocket-listings-staging')
#   local('heroku config:set TWITTER_SECRET=aGGBdl6LaFlF6gJkv1n2QRYarpVAYe3NSCjF0hg1L4 --app rocket-listings-staging')
>>>>>>> Apparently the lastest version of psycopg2 breaks django postgres pool
