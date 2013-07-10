from fabric.api import local,env

def resetdb(db=env.get('user')):
  local('dropdb -h localhost %s' % db)
  local('createdb -h localhost %s' % db)
  local('python manage.py syncdb --noinput --migrate')
  local('python manage.py loaddata messages_demo.yaml')
