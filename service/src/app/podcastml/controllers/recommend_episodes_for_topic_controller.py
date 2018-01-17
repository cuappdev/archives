from . import *

class RecommendEpisodesForTopicController(AppDevController):

  def get_path(self):
    return '/episodes/topic/<topic_id>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    topic_id = request.view_args['topic_id']
    episode_ids = episodes_for_topic_dao.get_episodes_list_for_topic(topic_id)
    return {'episode_ids': episode_ids}
