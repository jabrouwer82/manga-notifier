import webapp2
import configuration

from webapp2_extras import routes

application = webapp2.WSGIApplication([
    webapp2.Route('/',
                  handler='manga.MangaList',
                  name='home'),
    routes.RedirectRoute('/manga',
                         handler='manga.Manga',
                         name='add-manga',
                         strict_slash=True),
    routes.PathPrefixRoute('/manga', [
        routes.RedirectRoute('/delete',
                             handler='manga.MangaDelete',
                             name='delete-manga',
                             strict_slash=True),
        routes.RedirectRoute('/list',
                             handler='manga.MangaList',
                             name='list-manga',
                             strict_slash=True),
        routes.RedirectRoute('/<ident>',
                             handler='manga.Manga',
                             name='edit-manga',
                             strict_slash=True)
    ]),
    routes.RedirectRoute('/schedule',
                         handler='schedule.Schedule',
                         name='schedule',
                         strict_slash=True),
    routes.RedirectRoute('/update',
                         handler='update.UpdateAll',
                         name='update-all',
                         strict_slash=True),
    routes.PathPrefixRoute('/update', [
        routes.RedirectRoute('/update/cancel',
                             handler='update.Cancel',
                             name='update-cancel',
                             strict_slash=True),
        routes.RedirectRoute('/update/<ident>',
                             handler='update.UpdateOne',
                             name='update-manga',
                             strict_slash=True)
    ]),
    routes.RedirectRoute('/convert',
                         handler='converter.Converter',
                         name='converter',
                         strict_slash=True)
], debug=True)
