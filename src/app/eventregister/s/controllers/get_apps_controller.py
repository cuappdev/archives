from . import *

class GetAppsController(AppDevController):
  def get_path(self):
    return '/apps/'

  def get_methods(self):
    return ['GET']

  @authorize_user
  def content(self, **kwargs):
    user = kwargs.get('user')
    app_ids = users_dao.get_users_apps(user.id)
    apps = []

    for app_id in app_ids:
      apps.append(applications_dao.get_app_by_id(app_id))

    return apps
