from . import *

class GetEventsController(AppDevController):
  def get_path(self):
    return '/apps/<app_id>/events/'

  def get_methods(self):
    return ['GET']

  @authorize_user
  def content(self, **kwargs):
    user = kwargs.get('user')
    app_id = request.view_args['app_id']

    try:
      if int(app_id) not in {app.id for app in \
                             users_dao.get_user_apps(user.id)}:
        raise Exception('User not authorized for this app.')

      return [event.serialize() for event in \
              applications_dao.get_events(app_id)]
    except ValueError:
      raise Exception('Invalid app ID.')
