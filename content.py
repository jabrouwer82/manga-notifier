import logging
import urllib2

from urlparse import urlparse

from models import ContentSource
from utils import format_url

class Content(object):
  def __init__(self, url_scheme, volume, chapter):
    self.volume = volume
    self.chapter = chapter
    self.url_scheme = url_scheme
    self.url = format_url(url_scheme, volume, chapter) 
    self.page = urllib2.urlopen(self.url).read().decode('UTF-8')
    source = self.source_name()
    self.source = ContentSource.query(ContentSource.name == source).get()

  def update(self, volume=None, chapter=None):
    if volume:
      self.volume = volume
    if chapter:
      self.chapter = chapter
    self.url = format_url(self.url_scheme, volume, chapter) 
    self.page = urllib2.urlopen(self.url).read().decode('UTF-8')
  
  def is_not_found(self):
    if self.source:
      return self.source.not_found in self.page
    else:
      return False
      
  def page_count(self):
    if self.source:
      for num in xrange(1, 100):
        if not self.source.page_count.format(num=num) in self.page:
          return num - 1
    return 100

  def source_name(self):
    domain = urlparse(self.url).hostname
    # Assumes the form 'sub.domain.tld' in which case we want domain
    return domain.split('.')[-2]
    
