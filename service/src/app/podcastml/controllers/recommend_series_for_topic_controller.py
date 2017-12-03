from . import *

class RecommendSeriesForTopicController(AppDevController):

  def get_path(self):
    return '/series/topic/<topic_id>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    topic_id = request.view_args['topic_id']
    series_ids = series_for_topic_dao.get_series_list_for_topic(topic_id)
    return {'series_ids': series_ids}
