import logging

from mail import send_mail
from utils import Handler
from google.appengine.ext import ndb
from models import Manga as MangaModel

class Manga(Handler):

  def get(self):
    url_key = self.request.get('manga', '')
    if url_key:
      key = ndb.Key(urlsafe=url_key)
      manga = key.get()
      manga.url_key = key.urlsafe()
      # This is for the hidden input on the template.
    else:
      manga = MangaModel()
    self.render_template('manga.html', manga=manga)

  def post(self):
    url_key = self.request.get('key', '')
    if url_key:
      key = ndb.Key(urlsafe=url_key)
      manga = key.get()
    else:
      manga = MangaModel()
    manga.name = self.request.get('name', '')
    manga.frequency = float(self.request.get('frequency', ''))
    manga.url_scheme = self.request.get('url_scheme', '')
    manga.volume = [int(x) for x in self.request.get('volume', '').split(',')]
    manga.freq_units = self.request.get('freq_units', '')
    manga.countdown = float(self.request.get('countdown', ''))
    manga.update = bool(self.request.get('update', False))
    manga.manga_updates_url = self.request.get('manga_updates_url', '')
    key = manga.put()
    self.response.write(key.urlsafe())

class MangaDelete(Handler):
  def get(self):
    url_key = self.request.get('manga', '')
    key = ndb.Key(urlsafe=url_key)
    manga = key.get()
    subject = 'Deleted {manga} from datastore'.format(manga=manga.name)
    html_message = self.render_template('delete_email.html', write=False, manga=manga)
    send_mail(subject, html=html_message)
    self.response.write(html_message)
    key.delete()

class MangaList(Handler):
  def get(self):
    manga = MangaModel.query()
    self.render_template('manga_list.html', mangas=manga)
