from . import *
import traceback

class CreateEventTypeController(AppDevController):
  def get_path(self):
    return '/apps/<app_id>/event_types/create/'

  def get_methods(self):
    return ['POST']

  @authorize_user
  def content(self, **kwargs):
    try:
      data = request.get_json()
      app_id = request.view_args['app_id']
      name = data.get('name')
      user = kwargs.get('user')
      fields_info = data.get('fields_info')

      if name is None or fields_info is None:
        raise Exception('Invalid event type name or field descriptor.')

      event_types_dao.verify_fields_info(fields_info)
      created, event_type = event_types_dao.create_event_type(app_id, name,
                                                              user.id,
                                                              fields_info)

      if not created:
        raise Exception('Event type already exists.')

      return {}
    except Exception:
      traceback.print_exc()
