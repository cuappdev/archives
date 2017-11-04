from . import *

class GetAppsController(AppDevController):
  def get_path(self):
    return '/apps/'

  def get_methods(self):
    return ['GET']

  @authorize_user
  def content(self, **kwargs):
    user = kwargs.get('user')
    return users_dao.get_users_apps(user.id)
