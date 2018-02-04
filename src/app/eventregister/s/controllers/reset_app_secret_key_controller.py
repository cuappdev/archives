from . import *

class ResetAppSecretKeyController(AppDevController):
  def get_path(self):
    return '/apps/<app_id>/reset_secret_key/'

  def get_methods(self):
    return ['POST']

  @authorize_user
  def content(self, **kwargs):
    data = request.get_json()
    app_id = request.view_args['app_id']

    return {"secret_key": applications_dao.reset_secret_key(app_id)}
