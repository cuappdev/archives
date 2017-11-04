from . import *

class UpdateSessionController(AppDevController):
  def get_path(self):
    return '/session/'

  def get_methods(self):
    return ['POST']

  @auth_bearer
  def content(self, **kwargs):
    update_token = kwargs.get('bearer_token')
    user = users_dao.get_user_by_update_token(update_token)

    if user is None or not user.verify_update_token(update_token):
      raise Exception('Invalid update token.')

    user.renew_session()
    return {'session_token': user.session_token,
            'session_expiration': user.session_expiration,
            'update_token': user.update_token}
