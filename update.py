import urllib2

from utils import Handler
from google.appengine.ext import ndb
from google.appengine.api import mail
from models import Manga
from itertools import count

class Update(Handler):

  def get(self):
    email = 'jabrouwerutil@gmail.com'
    query = Manga.query()
    for manga in query.fetch():
      if manga.countdown <= 0 and manga.update:
        name = manga.name
        url = manga.url_scheme.format(*manga.volume)
        message='''
Time for the next chapter of {name}! 

You can access it here: {url}.

If there is an isue with the url format, you can update it here:
http://ballin-octo-wallhack.appspot.com/manga?manga={key}

Or you can turn off updates for this manga by accessing the following link:
http://ballin-octo-wallhack.appspot.com/unsubscribe?manga={key}'''
        message = message.format(name=name, url=url, key=manga.key.urlsafe())
        subject = 'Time for {name}'.format(name=name)
        mail.send_mail_to_admins(email, subject, message)

        page = urllib2.urlopen(url).read()
        page_num = 50
        for x in count(1):
          if not '>{}<'.format(x) in page:
            page_num = x - 1
            break
          if x >= 70:
            break

        manga.countdown = int(manga.frequency * page_num)
        manga.volume[-1] += 1
        manga.put()
      else:
        manga.countdown -= 1
        manga.put()
