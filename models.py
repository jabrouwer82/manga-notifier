from google.appengine.ext import ndb

class BaseModel(ndb.Model):
  @classmethod
  def fetch_by_name(cls, name):
    item = cls.query(cls.name == name).get()
    return item

  @classmethod
  def fetch_by_key(cls, url_key):
    key = ndb.Key(urlsafe=url_key)
    item = key.get()
    return item

  @classmethod
  def fetch_by_name_or_key(cls, ident):
    item = cls.fetch_by_name(ident)
    if not item:
      item = cls.fetch_by_key(ident)
    return item

  @classmethod
  def fetch_by_key_or_name(cls, ident):
    item = cls.fetch_by_key(ident)
    if not item:
      item = cls.fetch_by_name(ident)
    return item


class Manga(BaseModel):
  '''Models a manga.'''

  name = ndb.StringProperty(default='')
  url_scheme = ndb.StringProperty(default='')
  volume = ndb.IntegerProperty(default=-1)
  chapter = ndb.IntegerProperty(default=0)
  frequency = ndb.FloatProperty(default=1.0)
  freq_units = ndb.StringProperty(default='')
  countdown = ndb.FloatProperty(default=0.0)
  manga_updates_url = ndb.StringProperty(default='')

class ContentSource(BaseModel):
  name = ndb.StringProperty(default='')
  chapter = ndb.StringProperty(default='')
  page = ndb.StringProperty(default='')
  not_found = ndb.StringProperty(default='')
  
