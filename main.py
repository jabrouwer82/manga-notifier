import webapp2
import configuration

from manga import Manga, MangaDelete, MangaList
from schedule import Schedule
from update import UpdateAll, UpdateOne

application = webapp2.WSGIApplication([
    ('/', MangaList),
    ('/manga', Manga),
    ('/manga/delete', MangaDelete),
    ('/manga/list', MangaList),
    ('/manga/update', UpdateOne),
    ('/schedule', Schedule),
    ('/update', UpdateAll)
], debug=True)
