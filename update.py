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

  def url_format(self, url, volume, chapter):
     if volume >= 0:
       return url.format(volume, chapter)
     else:
       return url.format(chapter)

  def update(self, manga):
    if manga.countdown < 1:
      name = manga.name
      url = self.url_format(manga.url_scheme, manga.volume, manga.chapter)
      manga.chapter += 1
      next_url = self.url_format(manga.url_scheme, manga.volume, manga.chapter)
      manga_updates_url = manga.manga_updates_url
      
      # Determine the next countdown
      page = urllib2.urlopen(next_url).read()
      page_num = 50
      page_error = False
      if 'not available yet' in page and len(manga.volume) == 2:
        # Either the volume is incorrect or we're all caught up.
        new_volume = manga.volume
        new_volume += 1
        next_url = self.url_format(manga.url_scheme, manga.volume, manga.chapter)
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
      manga.countdown = min(max(manga.countdown, 0.0), 18.0)
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
    for manga in query:
      try:
        self.update(manga)
      except HTTPError:
        logging.error('Error while updating {manga}'.format(manga=manga.name))
        raise

class UpdateOne(Update):
  def get(self):
    url_key = self.request.get('manga', '')
    key = ndb.Key(urlsafe=url_key)
    manga = key.get()
    self.update(manga)

