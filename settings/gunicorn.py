from multiprocessing import cpu_count
from os import environ

bind = '0.0.0.0:' + os.environ.get('PORT', '8000')
workers = cpu_count() * 2 + 1
max_requests = 10000
worker_class = "gevent"

def def_post_fork(server, worker):
    from settings.psyco_gevent import make_psycopg_green
    make_psycopg_green()
    worker.log.info("Made Psycopg Green")

post_fork = def_post_fork