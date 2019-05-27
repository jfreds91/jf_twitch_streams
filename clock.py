from apscheduler.schedulers.blocking import BlockingScheduler
import os
from wrangling_scripts.sql_update import kickoff_sql_thread
from rq import Queue
from worker import rq_conn



def testing1():
    print('########## kicking off scheduled job ############')
    DATABASE_URL = os.environ['DATABASE_URL']
    
    q = Queue(connection = rq_conn)
    q.enqueue(kickoff_sql_thread, DATABASE_URL)
    
if __name__ == '__main__':
    #from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
        
    sched.add_job(testing1, 'cron', id='run_on_interval', minute='*/1')
        
sched.start()