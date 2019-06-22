from . import *

class CreateAppController(AppDevController):
  def get_path(self):
    return '/apps/create/'

  def get_methods(self):
    return ['POST']

  @authorize_user
  def content(self, **kwargs):
    data = request.get_json()
    app_name = data.get('app_name')
    user = kwargs.get('user')

    if app_name is None or app_name == '':
      raise Exception('Invalid app name.')

    created, app = applications_dao.create_app(app_name, user.id)

    if not created:
      raise Exception('App name in use.')

    return app.serialize()
