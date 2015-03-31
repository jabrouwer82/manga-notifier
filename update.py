import urllib2
import datetime

from utils import Handler
from google.appengine.ext import ndb
from google.appengine.api import mail
from models import Manga
from itertools import count
from google.appengine.api import taskqueue

class Update(Handler):

  def get(self):
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    taskqueue.add(url='/update', eta=tomorrow, method='GET')
    email = 'jabrouwerutil@gmail.com'
    query = Manga.query()
    query.filter('update=', True)
    for manga in query.fetch():
      if manga.countdown < 1 and manga.update:
        name = manga.name
        url = manga.url_scheme.format(*manga.volume)
        manga_updates_url = manga.manga_updates_url
        
        # Determine the next countdown
        page = urllib2.urlopen(url).read()
        page_num = 50
        for x in count(1):
          if not '>{}<'.format(x) in page:
            page_num = x - 1
            break
          if x >= 70:
            break

        if manga.freq_units == 'pages':
          countdown = manga.frequency * page_num
        elif manga.freq_unit == 'days':
          countdown = manga.frequency
        manga.countdown += countdown
        manga.volume[-1] += 1
        manga.put()
        
        # Send the email
        message='''
Time for the next chapter of {name}! 

You can access it here: {url}.

You will receive the next update for {name} in {countdown} days.

For more information on this manga, see: {manga_updates_url}.

If there is an isue with this manga status, you can update it here:
http://ballin-octo-wallhack.appspot.com/manga?manga={key}'''
        message = message.format(name=name, url=url, key=manga.key.urlsafe(), countdown=countdown, manga_updates_url=manga_updates_url)
        subject = 'Time for {name}'.format(name=name)
        mail.send_mail_to_admins(email, subject, message)
      else:
        manga.countdown -= 1
        manga.put()
