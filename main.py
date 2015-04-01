import webapp2

from manga import Manga, MangaDelete
from update import UpdateAll, UpdateOne

application = webapp2.WSGIApplication([
    ('/manga', Manga),
    ('/manga/update', UpdateOne),
    ('/manga/delete', MangaDelete),
    ('/update', UpdateAll)
], debug=True)
