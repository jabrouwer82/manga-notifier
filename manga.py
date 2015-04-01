import logging
from utils import Handler
from google.appengine.ext import ndb
from models import Manga as MangaModel


class Manga(Handler):

  def get(self):
    url_key = self.request.get('manga', '')
    if url_key and not url_key == '/':
      # When making a new manga, the url_key argument isn't filled out.
      # However jinja changes that from an empty string to a '/' for some reason.
      key = ndb.Key(urlsafe=url_key)
      manga = key.get()
      manga.url_key = key.urlsafe()
    else:
      manga = MangaModel()
    manga = {'manga': manga}
    self.render_template('manga.html', manga)

  def post(self):
    url_key = self.request.get('key', '')
    if url_key and not url_key == '/':
      # When making a new manga, the url_key argument isn't filled out.
      # However jinja changes that from an empty string to a '/' for some reason.
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

