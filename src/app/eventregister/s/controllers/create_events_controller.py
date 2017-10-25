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
    succeeded, failed = events_dao.create_events(app.id, events)
    return {'succeeded': succeeded, 'failed': failed}
