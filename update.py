import urllib2
import datetime
import logging

from google.appengine.ext import ndb
from itertools import count
from mail import send_mail
from models import Manga
from schedule import Schedule
from utils import Handler

class Update(Handler):
  def update(self, manga):
    if manga.countdown < 1:
      name = manga.name
      url = manga.url_scheme.format(*manga.volume)
      manga.volume[-1] += 1
      next_url = manga.url_scheme.format(*manga.volume)
      manga_updates_url = manga.manga_updates_url
      
      # Determine the next countdown
      page = urllib2.urlopen(next_url).read()
      page_num = 50
      page_error = False
      if 'not available yet' in page and len(manga.volume) == 2:
        # Either the volume is incorrect or we're all caught up.
        new_volume = manga.volume
        new_volume[0] += 1
        next_url = manga.url_scheme.format(*new_volume)
        page = urllib2.urlopen(next_url).read()
        if not 'not available yet' in page:
          manga.volume = new_volume
      
      if 'not available yet' in page:
        # Either we don't have a volume to adjust or the volume adjust
        # doesn't fix the page error.
        logging.error('Page error, manga not found at {url}'.format(url=next_url))
        page = ''
        page_error = True


      if page:
        for x in count(1):
          if not '>{num}<'.format(num=x) in page:
            page_num = x - 1
            break
          if x >= 70:
            break

      if page_error:
        countdown = 0
      elif manga.freq_units == 'pages':
        countdown = manga.frequency * page_num
      elif manga.freq_units == 'days':
        countdown = manga.frequency
      else:
        logging.warning('Manga {manga} missing freq_units'.format(manga=name))
        countdown = manga.frequency * page_num
      manga.countdown = countdown + manga.countdown if manga.countdown else countdown
      manga.put()
      
      # Send the email
      message='''
Time for the next chapter of {name}! 

You can access it here: {url}.

You will receive the next update for {name} in {countdown} days.

For more information on this manga, see: {manga_updates_url}.

If there is an isue with this manga status, you can update it here:
http://ballin-octo-wallhack.appspot.com/manga?manga={key}'''
      message = message.format(name=name, url=url, key=manga.key.urlsafe(), countdown=manga.countdown, manga_updates_url=manga_updates_url)
      subject = 'Time for {name}'.format(name=name)
      send_mail(subject, message)
    else:
      manga.countdown -= 1
      manga.put()

class UpdateAll(Update):
  def get(self):
    Schedule.schedule_update()
    query = Manga.query()
    # That was disgusting, why must I explicitly check for true
    for manga in query:
      self.update(manga)

class UpdateOne(Update):
  def get(self):
    url_key = self.request.get('manga', '')
    key = ndb.Key(urlsafe=url_key)
    manga = key.get()
    self.update(manga)

