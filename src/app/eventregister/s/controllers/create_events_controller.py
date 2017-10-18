from . import *

class CreateEventsController(AppDevController):
  def get_path(self):
    return '/events/'

  def get_methods(self):
    return ['POST']

  @authorize_app
  def content(self, **kwargs):
    app = kwargs.get('app')
    events = kwargs.get('events')
    succeeded = []
    failed = []

    for event in events:
      event_type = event_types_dao.get_event_type_by_name(app.id,
                                                          event['event_type'])
      created, event = events_dao.create_event(event_type.id, event['payload'])

      if created:
        succeeded.append(event_schema.dump(event).data)
      else:
        failed.append({'message': event, 'event': event})

    return {'succeeded': succeeded, 'failed': failed}
