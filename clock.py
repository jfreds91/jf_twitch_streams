from apscheduler.schedulers.blocking import BlockingScheduler
#import os



def testing1():
    print('test output!')
    
if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
        
    sched.add_job(testing1, 'cron', id='run_on_interval', minute='*/1')
        
sched.start()