from testcase import *
from app.podcastml.dao import series_for_topic_dao
from app.podcastml.itunes_top_series_fetcher import overall_top_id

class SeriesForTopicTestCase(TestCase):

  def setUp(self):
    super(SeriesForTopicTestCase, self).setUp()
    SeriesForTopic.query.delete()
    db_session_commit()

  def test_model_creation(self):
    series_for_topic_dao.generate_series_for_topics()
    self.assertTrue(SeriesForTopic.query.count() > 0)
    response = self.get('/api/v1/series/topic/all/')
    self.assertIsNotNone(json.loads(response.data)['data']['series_ids'])

  def test_endpoint(self):
    self.validate_model_retreival('/api/v1/series/topic', SeriesForTopic,
                                  ['topic_id', 'series_list'], 'series_ids')
