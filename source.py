import logging
import webapp2

from utils import Handler
from google.appengine.ext import ndb
from models import ContentSource

class Source(Handler):

  def get(self, ident=None):
    if ident:
      source = ContentSource.fetch_by_name_or_key(ident)
    
    # If we were not given a source or could not find the one we were given.
    if not ident or not source:
      source = ContentSource()
    
    self.render_template('source.html', source=source)

  def post(self, ident=None):
    if ident:
      source = ContentSource.fetch_by_key(ident)
    else:
      source = ContentSource()
    source.name = self.request.get('name', '')
    source.chapter = self.request.get('chapter', '')
    source.page = self.request.get('page', '')
    source.not_found = self.request.get('not_found', '')
    key = source.put()
    self.response.write(key.urlsafe())
    self.redirect(webapp2.uri_for('home'))

class SourceDelete(Handler):
  def get(self, ident):
    source = ContentSource.fetch_by_key(ident)
    subject = 'Deleted {source.name} from datastore'.format(source=source)
    html_message = self.render_template('delete_email.html', write=False, source=source)
    send_mail(subject, html=html_message)
    self.response.write(html_message)
    source.key.delete()
    self.redirect(webapp2.uri_for('home'))

class SourceList(Handler):
  def get(self):
    sources = ContentSource.query().fetch()
    self.render_template('source_list.html', sources=sources)
