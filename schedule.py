import logging

from datetime import date, datetime, time, timedelta
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import TaskRetryOptions, TombstonedTaskError
from utils import Handler
from mail import send_mail

class Schedule(Handler):
  @staticmethod
  def schedule_update(schedule_date=None, force=False):
    # Internal access for adding to the task queue
    if not schedule_date:
      schedule_date = date.today() + timedelta(days=1)
    four_thirty_am = time(9, 30)
    # 4:30 am CST is 9:30am UTC.
    # This leaves plenty of error room for not screwing up dates.
    schedule_time = datetime.combine(schedule_date, four_thirty_am)
    args = {'url': '/update',
            'eta': schedule_time,
            'method': 'GET'
           }
    if force:
      # In default queue with no name, to force a new update to run at the given time
      args['retry_options'] = TaskRetryOptions(task_retry_limit=0)
    else:
      # In restricts updatequeue to enforce one push per day
      args['name'] = str(schedule_date)
      args['queue_name'] = 'updatequeue'
    try:
      taskqueue.add(**args)
    except TombstonedTaskError, e:
      subject = 'Duplicate task created at manga-notifier'
      message = 'A task was created for {date} but there already exists a task for {date}.'.format(date=schedule_date)
      send_mail(subject, message)
      logging.exception('Duplicate task created')

  def get(self):
    # Endpoit handler for adding to the task queue
    schedule_date = self.request.get('date')
    force = bool(self.request.get('force', ''))
    if schedule_date:
      schedule_date = datetime.strptime(schedule_date, '%m-%d-%Y').date()
    Schedule.schedule_update(schedule_date, force)
