import webapp2

from manga import Manga, MangaDelete
from schedule import Schedule
from update import UpdateAll, UpdateOne

application = webapp2.WSGIApplication([
    ('/manga', Manga),
    ('/manga/update', UpdateOne),
    ('/manga/delete', MangaDelete),
    ('/schedule', Schedule),
    ('/update', UpdateAll)
], debug=True)
