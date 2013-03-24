import multiprocessing
import os
# import sys
# from path import path

# SITE_ROOT = path(__file__).abspath().dirname().dirname()

# sys.path.append(SITE_ROOT)
# sys.path.append(SITE_ROOT / 'apps')

port = os.environ.get("PORT", 5000)
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"

def def_post_fork(server, worker):
    from apps.rocketlistings.psyco_gevent import make_psycopg_green
    make_psycopg_green()
    worker.log.info("Made Psycopg Green")

post_fork = def_post_fork