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

    if app_id not in users_dao.get_users_apps(user.id):
      raise Exception('User not authorized for this app.')
    
    event_types = applications_dao.get_event_types(app_id)
    events = {}
    
    for event_type_id in event_types:
      event_type_name = event_types_dao.get_event_type_by_id(event_type_id).name
      event_ids = event_types_dao.get_events(event_type_id)
      event_type_events = [events_dao.get_event_by_id(event_id) for event_id in event_ids]
      events[event_type_name] = event_type_events

    return {'events': events}
