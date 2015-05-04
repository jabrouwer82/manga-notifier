from google.appengine.ext import ndb

class Manga(ndb.Model):
  '''Models a manga.'''

  name = ndb.StringProperty(default='')
  url_scheme = ndb.StringProperty(default='')
  volume = ndb.IntegerProperty(default=-1)
  chapter = ndb.IntegerProperty(default=0)
  frequency = ndb.FloatProperty(default=1.0)
  freq_units = ndb.StringProperty(default='')
  countdown = ndb.FloatProperty(default=0.0)
  manga_updates_url = ndb.StringProperty(default='')

  @classmethod
  def fetch_by_name(cls, name):
    manga = Manga.query(Manga.name == name).get()
    return manga

  @classmethod
  def fetch_by_key(cls, url_key):
    key = ndb.Key(urlsafe=url_key)
    manga = key.get()
    return manga
