from . import *

class ResetAppSecretKeyController(AppDevController):
  def get_path(self):
    return '/apps/<app_id>/reset/'

  def get_methods(self):
    return ['POST']

  @authorize_user
  def content(self, **kwargs):
    user = kwargs.get('user')
    app_id = request.view_args['app_id']

    try:
      if int(app_id) not in {app.id for app in \
                             users_dao.get_user_apps(user.id)}:
        raise Exception('User not authorized for this app.')

      params = request.args
      return {"secret_key": applications_dao.reset_secret_key(app_id)}
    except ValueError:
      raise Exception('Invalid app ID.')
