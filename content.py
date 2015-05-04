import urllib2

from collections import namedtuple
from utils import format_url

Source = namedtuple('Source', ['name', 'chapter_count', 'page_count', 'not_found'])

class Content(object):
  SOURCES = [
      Source('mangahere', '', '>{num}<', 'not available yet'),
      Source('readmanga', '>Chapter {num}<', '>Go to page {num}<', 'does not exist')
  ]

  def __init__(self, url_scheme, volume, chapter):
    self.volume = volume
    self.chapter = chapter
    self.url = format_url(url_scheme, volume, chapter) 
    self.page = urllib2.urlopen(self.url).read()
    for source in self.SOURCES:
      if source.name in self.url:
        self.source = source
        break
    else:
      self.source = None

  def is_not_found(self):
    return self.source.not_found in self.page
      
  def get_source(self):
    for source in self.SOURCES:
      if source.name in self.url:
        return source
    return None

  def page_count(self):
    for num in xrange(1, 100):
      if not self.source.page_count.format(num=num) in self.page:
        return num - 1
    return 100

