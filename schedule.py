import logging
import webapp2

from datetime import date, datetime, time, timedelta
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import TaskRetryOptions
from utils import Handler
from mail import send_mail

class Schedule(Handler):
  @staticmethod
  def schedule_update(schedule_date=None, schedule_time=None, force=False):
    # Internal access for adding to the task queue
    if not schedule_date:
      schedule_date = date.today() + timedelta(days=1)
    if not schedule_time:
      schedule_time = '4:30'
    hour, minute = map(int, schedule_time.split(':'))
    # Converts from EST to UTC by default.
    hour += 5
    # Account for drifting into the next UTC day
    if hour > 24:
      hour -= 24
      schedule_date += timedelta(days=1)
    schedule_time = time(hour, minute)
    # This leaves plenty of error room for not screwing up dates.
    schedule_datetime = datetime.combine(schedule_date, schedule_time)
    args = {'url': '/update',
            'eta': schedule_datetime,
            'method': 'GET'
           }
    if force:
      # In default queue with no name, to force a new update to run at the given time
      args['retry_options'] = TaskRetryOptions(task_retry_limit=0)
    else:
      # In restricts updatequeue to enforce one push per day
      args['name'] = str(schedule_date)
      args['queue_name'] = 'updatequeue'
    taskqueue.add(**args)

  def get(self):
    # Endpoit handler for adding to the task queue
    schedule_date = self.request.get('date')
    schedule_time = self.request.get('time')
    force = self.request.get('force')
    if schedule_date:
      schedule_date = datetime.strptime(schedule_date, '%m-%d-%Y').date()
    Schedule.schedule_update(schedule_date, schedule_time, force)
    self.redirect(webapp2.uri_for('home'))

