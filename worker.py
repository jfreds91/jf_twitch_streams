# This is the worker function which will run in the background to update the sql database
import redis
from rq import Worker, Queue, Connection
import os

listen = ['high', 'default', 'low']

# unsure what port to be using. Might actually be 29909
# added /0 per stack overflow?
# trying no port?
# trying redistogo
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

rq_conn = redis.from_url(redis_url)

if __name__ =='__main__':
    with Connection(re_conn):
        worker = Worker(map(Queue, listen))
        worker.work()