import multiprocessing

# bind = "0.0.0.0:$PORT"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"

def def_post_fork(server, worker):
    from rocketlistings.psyco_gevent import make_psycopg_green
    make_psycopg_green()
    worker.log.info("Made Psycopg Green")

post_fork = def_post_fork