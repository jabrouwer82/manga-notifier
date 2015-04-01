# This file contains helpful "tools" that other files can import and use
import jinja2
import os
import webapp2

from google.appengine.api import mail

EMAIL = 'jabrouwerutil@gmail.com'

jinja_environment = jinja2.Environment(
    autoescape=True,
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')
    )
)


class Handler(webapp2.RequestHandler):

  def render_template(self, template_name, contents):
    template = jinja_environment.get_template(template_name)
    self.response.out.write(template.render(contents))

  def render_json(self, json_txt):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json_txt)

  def handle_exception(self, exception, debug_mode):
    mail.send_mail_to_admins(EMAIL, 'Exception in manga notifier', exception)
    webapp2.RequestHandler.handle_exception(self, exception, debug_mode)
