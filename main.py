import manga
import webapp2

application = webapp2.WSGIApplication([
    ('/manga', manga.Manga)
], debug=True)
