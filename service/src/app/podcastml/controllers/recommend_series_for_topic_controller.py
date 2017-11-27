from . import *

class RecommendSeriesForTopicController(AppDevController):

  def get_path(self):
    return '/series/topic/<topic_name>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    topic_name = request.view_args['topic_name']
    # TODO: retrieve recommended series for this topic
    return {'message': 'recommend series for topic {}'.format(topic_name)}
