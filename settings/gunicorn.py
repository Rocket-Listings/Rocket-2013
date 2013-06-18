import multiprocessing 
#import os
# compensating for weird directory structure
# import sys
# SITE_ROOT = path(__file__).abspath().dirname()
# sys.path.append(SITE_ROOT)
# sys.path.append(SITE_ROOT / 'apps')

#bind = '0.0.0.0:' + os.environ.get('PORT', '8000')
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"

def def_post_fork(server, worker):
    from settings.psyco_gevent import make_psycopg_green
    make_psycopg_green()
    worker.log.info("Made Psycopg Green")

post_fork = def_post_fork