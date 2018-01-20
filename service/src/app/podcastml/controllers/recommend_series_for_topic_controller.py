from app.podcastml.itunes_top_series_fetcher import overall_top_id
from . import *

overall_top_url_key = 'all'

class RecommendSeriesForTopicController(AppDevController):

  def get_path(self):
    return '/series/topic/<topic_id>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    topic_id = request.view_args['topic_id']
    topic_id = overall_top_id if topic_id == overall_top_url_key else topic_id
    series_ids = series_for_topic_dao.get_series_list_for_topic(topic_id)
    return {'series_ids': series_ids}
