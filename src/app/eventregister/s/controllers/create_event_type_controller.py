from . import *

class CreateEventTypeController(AppDevController):
  def get_path(self):
    return '/apps/<app_id>/event_types/'

  def get_methods(self):
    return ['POST']

  @authorize_user
  def content(self, **kwargs):
    app_id = request.view_args['app_id']
    name = kwargs.get('name')
    user = kwargs.get('user')
    fields_info = kwargs.get('fields_info')

    event_types_dao.verify_fields_info(fields_info)
    created, event_type = event_types_dao.create_event_type(app_id, name,
                                                            user.id,
                                                            fields_info)

    if not created:
      raise Exception('Event type already exists.')
    
    return {'event_type': event_type}
