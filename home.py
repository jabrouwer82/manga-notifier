import logging
import webapp2

from mail import send_mail
from utils import Handler
from google.appengine.ext import ndb
from models import Manga

class Home(Handler):
  def get(self):
    manga = Manga.query(Manga.countdown < 1.0).fetch()
    self.render_template('home.html', mangas=manga)
