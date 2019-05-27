from apscheduler.schedulers.blocking import BlockingScheduler
import os



def testing1():
    print('attemping to get getdatabase env var')
    DATABASE_URL = os.environ['DATABASE_URL']
    print(DATABASE_URL)
    
if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
        
    sched.add_job(testing1, 'cron', id='run_on_interval', minute='*/1')
        
sched.start()