import webapp2
import configuration

from webapp2_extras import routes

application = webapp2.WSGIApplication([
    webapp2.Route('/',
                  handler='home.Home',
                  name='home'),
    # Manga endpoints
    routes.RedirectRoute('/manga',
                         handler='manga.Manga',
                         name='manga-add',
                         strict_slash=True),
    routes.PathPrefixRoute('/manga', [
        routes.RedirectRoute('/list',
                             handler='manga.MangaList',
                             name='manga-list',
                             strict_slash=True),
        routes.RedirectRoute('/<ident>',
                             handler='manga.Manga',
                             name='manga-edit',
                             strict_slash=True),
        routes.RedirectRoute('/delete/<ident>',
                             handler='manga.MangaDelete',
                             name='manga-delete',
                             strict_slash=True),
        routes.RedirectRoute('/update/<ident>',
                             handler='update.UpdateOne',
                             name='manga-update',
                             strict_slash=True)
    ]),
    # Source endpoints
    routes.RedirectRoute('/source',
                         handler='source.Source',
                         name='source-add',
                         strict_slash=True),
    routes.PathPrefixRoute('/source', [
        routes.RedirectRoute('/list',
                             handler='source.SourceList',
                             name='source-list',
                             strict_slash=True),
        routes.RedirectRoute('/<ident>',
                             handler='source.Source',
                             name='source-edit',
                             strict_slash=True),
        routes.RedirectRoute('/delete/<ident>',
                             handler='source.SourceDelete',
                             name='source-delete',
                             strict_slash=True),
    ]),
    # Schedule endpoints
    routes.RedirectRoute('/schedule',
                         handler='schedule.Schedule',
                         name='schedule',
                         strict_slash=True),
    routes.PathPrefixRoute('/shcedule', [
        routes.RedirectRoute('/cancel',
                             handler='schedule.Schedule',
                             name='schedule-cancel',
                             strict_slash=True)
    ]),
    # Update endpoints
    routes.RedirectRoute('/update',
                         handler='update.UpdateAll',
                         name='update-all',
                         strict_slash=True),
    routes.PathPrefixRoute('/update', [
        routes.RedirectRoute('/schedule',
                             handler='schedule.Schedule',
                             name='update-schedule',
                             strict_slash=True),
        routes.RedirectRoute('/cancel',
                             handler='update.Cancel',
                             name='update-cancel',
                             strict_slash=True),
        routes.RedirectRoute('/<ident>',
                             handler='update.UpdateOne',
                             name='update-manga',
                             strict_slash=True),
        routes.RedirectRoute('/undo/<ident>',
                             handler='update.Undo',
                             name='update-undo',
                             strict_slash=True)
    ]),
    routes.RedirectRoute('/convert',
                         handler='converter.Converter',
                         name='convert',
                         strict_slash=True)
], debug=True)
