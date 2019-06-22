from . import *

class CreateEventsController(AppDevController):
  def get_path(self):
    return '/events/create/'

  def get_methods(self):
    return ['POST']

  @authorize_app
  def content(self, **kwargs):
    data = request.get_json()
    app = kwargs.get('app')
    events = data.get('events')

    if events is None:
      raise Exception('Invalid event list.')

    succeeded, failed = events_dao.create_events(app.id, events)
    return {'succeeded': [event.serialize() for event in succeeded],
            'failed': failed}
