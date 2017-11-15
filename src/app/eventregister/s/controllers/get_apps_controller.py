from . import *

class GetAppsController(AppDevController):
  def get_path(self):
    return '/apps/'

  def get_methods(self):
    return ['GET']

  @authorize_user
  def content(self, **kwargs):
    user = kwargs.get('user')
    return [app.as_dict() for app in users_dao.get_user_apps(user.id)]
