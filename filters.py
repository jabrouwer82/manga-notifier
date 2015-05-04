import webapp2

# This is nasty and for development purposes only, but I'm leaving it.
def members(manga):
  return str(dir(manga))

def uri(*args, **kwargs):
  return webapp2.uri_for(*args, **kwargs)
