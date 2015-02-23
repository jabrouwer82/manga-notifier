from google.appengine.ext import ndb

class Manga(ndb.Model):
    '''Models a manga.'''

    name = ndb.StringProperty()
    url_scheme = ndb.StringProperty()
    volume = ndb.IntegerProperty(repeated=True)
    frequency = ndb.FloatProperty()
    freq_unit = ndb.StringProperty()

