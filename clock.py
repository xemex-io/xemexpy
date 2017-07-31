from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from traceback import format_exc

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def timed_job():
    print('This job is run every hour.')
    url = "https://xemexpy.herokuapp.com/price"
    try:
      requests.get(url)
    except BaseException as ex:
      print(format_exc())
sched.start()
