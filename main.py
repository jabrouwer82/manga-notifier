import webapp2

from manga import Manga
from update import UpdateAll, UpdateOne

application = webapp2.WSGIApplication([
    ('/manga', Manga),
    ('/manga/update', UpdateOne),
    ('/update', UpdateAll)
], debug=True)
