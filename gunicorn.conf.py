# from multiprocessing import cpu_count
from os import environ

bind = '0.0.0.0:' + environ.get('PORT', '8000')
workers = 8 # cpu_count() * 2 + 1
max_requests = 1000
worker_class = "gevent"
timeout = 30
loglevel = "debug"
def def_post_fork(server, worker):
   from rocket.settings.psyco_gevent import make_psycopg_green
   make_psycopg_green()
   worker.log.info("Made Psycopg Green")

post_fork = def_post_fork