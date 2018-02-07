from . import *

class AuthenticateUserController(AppDevController):
  def get_path(self):
    return '/login/'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email is None or password is None:
      raise Exception('Invalid email or password.')

    success, user = users_dao.verify_credentials(email, password)

    if not success:
      raise Exception('Incorrect email or password.')

    return {'session_token': user.session_token,
            'session_expiration': str(user.session_expiration),
            'update_token': user.update_token}
