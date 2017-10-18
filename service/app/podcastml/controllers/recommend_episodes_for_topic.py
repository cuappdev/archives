from . import *

class RecommendEpisodesForTopicController(AppDevController):

  def get_path(self):
    return '/episodes/topic/<topic_name>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    topic_name = request.view_args['topic_name']
    # TODO: retrieve recommended episodes for this topic
    return {'message': 'recommend episodes for topic'}
