from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes = 1)
def timed_job():
    DATABASE_URL = os.environ['DATABASE_URL']
    print(DATABASE_URL)