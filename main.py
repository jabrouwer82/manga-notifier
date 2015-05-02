import webapp2
import configuration

from manga import Manga, MangaDelete, MangaList
from schedule import Schedule
from update import UpdateAll, UpdateOne

application = webapp2.WSGIApplication([
    webapp2.Route('/', MangaList),
    webapp2.Route('/manga', Manga),
    webapp2.Route('/manga/delete', MangaDelete),
    webapp2.Route('/manga/list', MangaList),
    webapp2.Route('/manga/update', UpdateOne),
    webapp2.Route('/manga/<ident>', Manga),
    webapp2.Route('/schedule', Schedule),
    webapp2.Route('/update', UpdateAll)
], debug=True)
