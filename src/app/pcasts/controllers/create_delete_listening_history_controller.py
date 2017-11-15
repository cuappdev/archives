from . import *

class CreateDeleteListeningHistoryController(AppDevController):

  def get_path(self):
    return '/history/listening/<episode_id>/'

  def get_methods(self):
    return ['DELETE']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    episode_id = request.view_args['episode_id']
    listening_history = listening_histories_dao.\
      delete_listening_history(episode_id, user)
    return {'listening_history': \
      listening_history_schema.dump(listening_history).data}
