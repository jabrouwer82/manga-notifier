import urllib2
import datetime
import logging

from google.appengine.ext import ndb
from itertools import count

from content import Content
from mail import send_mail
from models import Manga
from schedule import Schedule
from utils import Handler, format_url

class Update(Handler):

  def update(self, manga):
    if manga.countdown < 1:
      name = manga.name
      original_volume = manga.volume
      original_chapter = manga.chapter
      url = format_url(manga.url_scheme, original_volume, original_chapter)

      # Try current volume, next chapter
      volume = original_volume
      chapter = original_chapter + 1
      content = Content(manga.url_scheme, volume, chapter)
      if volume >= 0 and content.is_not_found():
        # Try next volume next chapter
        volume = original_volume + 1
        chapter = original_chapter + 1
        content = Content(manga.url_scheme, volume, chapter)
      if volume >= 0 and content.is_not_found():
        # Try next volume first chapter
        volume = original_volume + 1
        chapter = 1
        content = Content(manga.url_scheme, volume, chapter)
      if content.is_not_found():
        # Try current volume next next chapter
        volume = original_volume
        chapter = original_chapter + 2
        content = Content(manga.url_scheme, volume, chapter)
      if volume >= 0 and content.is_not_found():
        # Try next volume next next chapter
        volume = original_volume + 1
        chapter = original_chapter + 2
        content = Content(manga.url_scheme, volume, chapter)
      
      if content.is_not_found():
        # Something's goofed 
        manga.countdown = 0
        logging.error('Unable to update volume/chapter for {name}'.format(name=name))
      else:
        manga.volume = volume
        manga.chapter = chapter
        logging.info('Updating {name} from volume:{original_volume}, ' \
                     'chapter:{original_chapter} to volume:{volume}, chapter:{chapter}'
                     .format(name=name,
                             original_volume=original_volume,
                             original_chapter=original_chapter,
                             volume=volume,
                             chapter=chapter))
        # The next page checks out
        if manga.freq_units == 'pages':
          logging.info('{}, {}'.format(name, content.page_count()))
          manga.countdown += manga.frequency * content.page_count()
        elif manga.freq_units == 'days':
          manga.countdown += manga.frequency
        else:
          logging.warning('Manga {manga} missing freq_units'.format(manga=name))
          # Default acts like days.
          manga.countdown += manga.frequency

      # Assert 0 <= countdown <= 18
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
      message = message.format(name=name, url=url, key=manga.key.urlsafe(), countdown=manga.countdown, manga_updates_url=manga.manga_updates_url)
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
      except urllib2.HTTPError:
        logging.error('Error while updating {manga}'.format(manga=manga.name))
        raise

class UpdateOne(Update):
  def get(self):
    url_key = self.request.get('manga', '')
    key = ndb.Key(urlsafe=url_key)
    manga = key.get()
    self.update(manga)

