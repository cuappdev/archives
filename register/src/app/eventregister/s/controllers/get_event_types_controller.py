from . import *

class GetEventTypesController(AppDevController):
  def get_path(self):
    return '/apps/<app_id>/event_types/'

  def get_methods(self):
    return ['GET']

  @authorize_user
  def content(self, **kwargs):
    user = kwargs.get('user')
    app_id = request.view_args['app_id']

    try:
      if int(app_id) not in \
         {app.id for app in users_dao.get_user_apps(user.id)}:
        raise Exception('User not authorized for this app.')

      return [event_type.serialize() for event_type in \
              applications_dao.get_event_types(app_id)]
    except ValueError:
      raise Exception('Invalid app ID.')