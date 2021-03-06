import logging
import webapp2

from google.appengine.ext import ndb
from random import random

from mail import send_mail
from models import Manga as MangaModel
from utils import Handler

class Manga(Handler):

  def get(self, ident=None):
    if ident:
      manga = MangaModel.fetch_by_name_or_key(ident)
      seed = None

    # If we were not given a manga or could not find the one we were given.
    if not ident or not manga:
      manga = MangaModel()
      seed = random()
    
    self.render_template('manga.html', manga=manga, seed=seed)

  def post(self, ident=None):
    if ident:
      manga = MangaModel.fetch_by_key(ident)
    else:
      manga = MangaModel()
    manga.name = self.request.get('name', '')
    manga.frequency = float(self.request.get('frequency', ''))
    manga.url_scheme = self.request.get('url_scheme', '')
    manga.volume = int(self.request.get('volume', '-1'))
    manga.chapter = int(self.request.get('chapter', '-1'))
    manga.freq_units = self.request.get('freq_units', '')
    manga.countdown = float(self.request.get('countdown', ''))
    manga.update = bool(self.request.get('update', False))
    manga.manga_updates_url = self.request.get('manga_updates_url', '')
    key = manga.put()
    self.response.write(key.urlsafe())
    self.redirect(webapp2.uri_for('home'))

class MangaDelete(Handler):
  def get(self, ident):
    manga = MangaModel.fetch_by_key(ident)
    subject = 'Deleted {manga} from datastore'.format(manga=manga.name)
    html_message = self.render_template('delete_email.html', write=False, item=manga)
    send_mail(subject, html=html_message)
    self.response.write(html_message)
    manga.key.delete()
    self.redirect(webapp2.uri_for('home'))

class MangaList(Handler):
  def get(self):
    manga = MangaModel.query().fetch()
    self.render_template('manga_list.html', mangas=manga)
