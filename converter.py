from utils import Handler
from models import Manga

class Converter(Handler):

  def get(self):
    query = Manga.query()
    for manga in query:
      self.convert(manga)
      manga.put()

  def convert(self, manga):
    pass
