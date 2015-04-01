from google.appengine.ext import ndb

class Manga(ndb.Model):
    '''Models a manga.'''

    name = ndb.StringProperty(default='')
    url_scheme = ndb.StringProperty(default='')
    volume = ndb.IntegerProperty(repeated=True)
    frequency = ndb.FloatProperty(default=1.0)
    freq_units = ndb.StringProperty(default='')
    update = ndb.BooleanProperty(default=True)
    countdown = ndb.FloatProperty(default=0.0)
    manga_updates_url = ndb.StringProperty(default='')
