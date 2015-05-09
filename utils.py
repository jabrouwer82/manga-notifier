# This file contains helpful "tools" that other files can import and use
import logging
import webapp2

from google.appengine.api.taskqueue import TaskAlreadyExistsError, TombstonedTaskError
from google.appengine.ext import ndb

from mail import send_mail
from models import Manga
from configuration import jinja_env

EMAIL = 'jabrouwerutil@gmail.com'

def format_url(url_scheme, volume, chapter):
  if volume >= 0:
    return url_scheme.format(volume, chapter)
  else:
    return url_scheme.format(chapter)

class Handler(webapp2.RequestHandler):

  def render_template(self, template_name, write=True, **contents):
    template = jinja_env.get_template(template_name)
    if write:
      self.response.out.write(template.render(contents))
    else:
      return template.render(contents)

  def render_json(self, json_txt):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json_txt)

  def handle_exception(self, exception, debug_mode):
    if type(exception) in [TombstonedTaskError, TaskAlreadyExistsError]:
      subject = 'Duplicate task created at manga-notifier'
      message = repr(exception)
      send_mail(subject, message)
      logging.exception('Duplicate task created')
    else:
      send_mail('Exception in manga notifier', repr(exception))
      webapp2.RequestHandler.handle_exception(self, exception, debug_mode)
