import logging

from datetime import date, datetime, time, timedelta
from google.appengine.api import taskqueue
from models import Update
from utils import Handler

class Schedule(Handler):
  @staticmethod
  def can_update(prev_update=None):
    if not prev_update:
      prev_update = Update.query().fetch(1)
      if prev_update:
        prev_update = prev_update[0]
    
    if not prev_update or not prev_update.prev_update:
      return True
    
    if prev_update.prev_update < date.today():
      return True
    else:
      logging.info('Alread updated today')
      return False

  @staticmethod
  def schedule_update(schedule_date=None):
    # Internal access for adding to the task queue
    prev_update = Update.query().fetch(1)
    prev_update_is_new = False
    if prev_update:
      prev_update = prev_update[0]
    else:
      prev_update = Update()
      prev_update_is_new = True
    if Schedule.can_update(prev_update):
      if not schedule_date:
        schedule_date = date.today() + timedelta(days=1)
      four_thirty_am = time(9, 30)
      # 4:30 am CST is 9:30am UTC.
      # This leaves plenty of error room for not screwing up dates.
      schedule_time = datetime.combine(schedule_date, four_thirty_am)
      taskqueue.add(url='/update', eta=schedule_time, method='GET')
      prev_update.next_update = schedule_date
    if not prev_update_is_new:
      prev_update.prev_update = date.today()
    prev_update.put()

  def get(self):
    # Endpoit handler for adding to the task queue
    schedule_date = self.request.get('date')
    if schedule_date:
      schedule_date = datetime.strptime(schedule_date, '%m-%d-%Y').date()
    Schedule.schedule_update(schedule_date)
