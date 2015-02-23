import webapp2

from manga import Manga
from update import Update

application = webapp2.WSGIApplication([
    ('/manga', Manga),
    ('/update', Update)
], debug=True)
