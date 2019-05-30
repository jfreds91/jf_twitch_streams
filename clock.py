from apscheduler.schedulers.blocking import BlockingScheduler
import os
from wrangling_scripts.sql_update import get_sql_engine, scheduled_sql_task, recreate_table
import requests
#from rq import Queue
#from worker import rq_conn



def auto_update_sql_table(engine, DATABASE_URL):
    print('########## kicking off scheduled job ############')
    
    # get database url+
    DATABASE_URL = os.environ['DATABASE_URL']
    
    ##### Not run due to dyno constrictions on free heroku account... running on scheduler only #####
    #q = Queue(connection = rq_conn)
    #q.enqueue(kickoff_sql_thread, DATABASE_URL)
    
    # visit the website to keep the dyno from going idle
    requests.get('https://jf-streams-dash.herokuapp.com/')
    
    # run directly due to dyno limits preventing free worker
    engine = get_sql_engine(DATABASE_URL)
    recreate_table(DATABASE_URL, 'games_table')
    scheduled_sql_task(engine, 'games_table')
    
    # kill database connections
    #os.system('heroku ps:killall')
    engine.dispose()
    
if __name__ == '__main__':
    #from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    
    sched.add_job(auto_update_sql_table, 'cron', id='run_on_interval', minute='*/10')
        
sched.start()