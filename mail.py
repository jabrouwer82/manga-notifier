from google.appengine.api import mail

EMAIL = 'jabrouwerutil@gmail.com'

def send_mail(subject, message='', **kwargs):
  mail.send_mail_to_admins(EMAIL, subject, message, **kwargs)
