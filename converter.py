from utils import Handler
from models import Manga

class Converter(Handler):

  def get(self):
    query = Manga.query()
    for manga in query:
      self.convert(manga)
      manga.put()

  def convert(self, manga):
    manga.vol = -1
    manga.freq_unit = ''
    delattr(manga, 'vol')
    delattr(manga, 'freq_unit')
