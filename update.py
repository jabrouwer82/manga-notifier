import datetime
import logging
import urllib2
import webapp2
import threading

from google.appengine.api import taskqueue
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
        content.update(volume, chapter)
      if volume >= 0 and content.is_not_found():
        # Try next volume first chapter
        volume = original_volume + 1
        chapter = 1
        content.update(volume, chapter)
      if content.is_not_found():
        # Try current volume next next chapter
        volume = original_volume
        chapter = original_chapter + 2
        content.update(volume, chapter)
      if volume >= 0 and content.is_not_found():
        # Try next volume next next chapter
        volume = original_volume + 1
        chapter = original_chapter + 2
        content.update(volume, chapter)
      
      if content.is_not_found():
        # Something's goofed, try again tomorrow. 
        manga.countdown = float('-inf')
        logging.error('Unable to update volume/chapter for {name}'.format(name=name))
      else:
        manga.prev_volume = original_volume
        manga.prev_chapter = original_chapter
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
      if manga.countdown != float('-inf'):
        manga.countdown = min(max(manga.countdown, 0.0), 18.0)
      else:
        manga.countdown = -1.0
      manga.put()
      
      # Send the email
      message = self.render_template('update_email.html', manga=manga, write=False)
      if manga.volume >= 0:
        subject = 'Time for {manga.name} v{manga.volume}c{manga.chapter}'.format(manga=manga)
      else:
        subject = 'Time for {manga.name} c{manga.chapter}'.format(manga=manga)
      send_mail(subject, message)
    else:
      manga.countdown -= 1
      manga.put()

class UpdateAll(Update):
  def get(self):
    threading.Thread(target=Schedule.schedule_update).start()
    query = Manga.query()
    for manga in query:
      try:
        self.update(manga)
      except urllib2.HTTPError:
        logging.error('Error while updating {manga}'.format(manga=manga.name))
        raise
    self.redirect(webapp2.uri_for('home'))

class UpdateOne(Update):
  def get(self, ident):
    manga = Manga.fetch_by_name_or_key(ident)
    self.update(manga)
    self.redirect(webapp2.uri_for('home'))

class Cancel(Handler):
  def get(self):
    # Purge entire queue
    q = taskqueue.Queue('updatequeue')
    q.purge()
    q = taskqueue.Queue('default')
    q.purge()
    self.redirect(webapp2.uri_for('home'))

class Revert(Handler):
  def get(self, ident):
    manga = Manga.fetch_by_name_or_key(ident)
    chapter = int(self.request.get('chapter', -1))
    volume = int(self.request.get('volume', -1))
    if chapter > -1:
      manga.chapter = chapter
    if prev_volume > -1:
      manga.volume = volume
    manga.put()
    self.redirect(webapp2.uri_for('home'))

class Undo(Handler):
  def get(self, ident):
    manga = Manga.fetch_by_name_or_key(ident)
    if manga.prev_chapter >= 0:
      manga.chapter = manga.prev_chapter
      manga.prev_chapter = -1
    if manga.prev_volume >= 0:
      manga.volume = manga.prev_volume
      manga.prev_volume = -1
    manga.put()
    self.redirect(webapp2.uri_for('home'))
