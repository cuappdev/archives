from . import *

class RecommendEpisodesForUserController(AppDevController):

  def get_path(self):
    return '/episodes/user/<user_id>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user_id = request.view_args['user_id']
    episode_ids = episodes_for_user_dao.get_episodes_list_for_user(user_id)
    return {'episode_ids': episode_ids}
