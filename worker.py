# This is the worker function which will run in the background to update the sql database
import redis
from rq import Worker, Queue, Connection
import os

listen = ['high', 'default', 'low']

# unsure what port to be using. Might actually be 29909
# added /0 per stack overflow?
# trying no port?
# trying redistogo
# trying redis
# 29909 works but is not correct
# trying redistogo instead, provisioned redis togo and verified env var appears with heroku config
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

rq_conn = redis.from_url(redis_url)

if __name__ =='__main__':
    with Connection(rq_conn):
        worker = Worker(map(Queue, listen))
        worker.work()