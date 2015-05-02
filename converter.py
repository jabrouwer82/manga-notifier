from utils import Handler
from models import Manga

class Converter(Handler):

  def get(self):
    query = Manga.query()
    for manga in query:
      self.convert(manga)
      manga.put()

  def convert(self, manga):
    volume = manga.volume
    manga.chapter = volume[-1]
    if len(volume) == 2:
      manga.vol = volume[0]
    else:
      manga.vol = -1
    if manga.freq_unit:
      del manga.freq_unit
    if manga.volume:
      del manga.volume
