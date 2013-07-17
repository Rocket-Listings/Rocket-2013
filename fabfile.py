from fabric.api import local,env

def resetdb():
  local('rm rocket/default.db')
  local('python manage.py syncdb --noinput --migrate')
  local('python manage.py loaddata messages_demo.yaml')
