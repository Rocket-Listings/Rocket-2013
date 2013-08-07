from fabric_heroku_postgresql.core import *
from fabric.api import local,env

def resetdb():
  local('rm -f rocket/default.db')
  local('python manage.py syncdb --noinput --migrate')
  local('python manage.py loaddata messages_demo.yaml')
  local('python manage.py rebuild_index --noinput')
