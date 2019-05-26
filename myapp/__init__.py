from flask import Flask

app = Flask(__name__)

from myapp import routes

# import function to run continuous query, start thread
from wrangling_scripts.sql_update import kickoff_sql_thread, get_sql_engine
from rq import Queue
from worker import rq_conn

engine = get_sql_engine()

q = Queue(connection = rq_conn)
q.enqueue(kickoff_sql_thread, args=(engine,), 'http://heroku.com')
