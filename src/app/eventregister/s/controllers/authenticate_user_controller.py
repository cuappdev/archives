from . import *

class AuthenticateUserController(AppDevController):
  def get_path(self):
    return '/login/'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    email = kwargs.get('email')
    password = kwargs.get('password')

    success, user = users_dao.verify_credentials(email, password)

    if not success:
      raise Exception('Incorrect email or password.')

    return {'session_token': user.session_token, \
            'session_expiration': user.session_expiration}
