from . import *
import json

class CreateEventTypeController(AppDevController):
  def get_path(self):
    return '/apps/<app_id>/event_types/create/'

  def get_methods(self):
    return ['POST']

  @authorize_user
  def content(self, **kwargs):
    data = request.get_json()
    app_id = request.view_args['app_id']
    name = data.get('name')
    user = kwargs.get('user')
    fields_info_str = data.get('fields_info')
    fields_info = None

    if name is None or name == '' or fields_info_str is None:
      raise Exception('Invalid event type name or field descriptor.')

    try:
      print 'test'
      fields_info = json.loads(fields_info_str)
      print 'test2'
    except:
      raise Exception('Invalid event type name or field descriptor.')
      
    event_types_dao.verify_fields_info(fields_info)
    created, event_type = event_types_dao.create_event_type(app_id, name,
                                                            user.id,
                                                            fields_info)

    if not created:
      raise Exception('Event type already exists.')

    return event_type.serialize()

