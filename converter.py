from utils import Handler
from models import Manga

class Converter(Handler):

  def get(self):
    query = Manga.query()
    for manga in query:
      self.convert(manga)
      manga.put()

  def convert(self, manga):
    if 'freq_unit' in manga._properties:
      del manga.freq_unit
    if 'volume' in manga._properties and manga.volume:
      volume = manga.volume
      manga.chapter = volume[-1]
      if len(volume) == 2:
        manga.vol = volume[0]
      else:
        manga.vol = -1
      del manga.volume
