from . import *

class CreateAppController(AppDevController):
  def get_path(self):
    return '/apps/'

  def get_methods(self):
    return ['POST']

  @authorize_user
  def content(self, **kwargs):
    app_name = kwargs.get('app_name')
    user = kwargs.get('user')
    created, app = create_app(app_name, user.id)
    return {'created': created, 'app': app}
