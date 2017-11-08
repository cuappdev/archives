import json
import os
from testcase import *
from app.podcastml.dao import series_for_topic_dao

class SeriesForTopicTestCase(TestCase):

  def setUp(self):
    super(SeriesForTopicTestCase, self).setUp()
    SeriesForTopic.query.delete()
    db_session_commit()

  def test_endpoint(self):
    response = self.app.get('/api/v1/series/topic/hi/',
                            headers=self.api_key_header)
    data = json.loads(response.data)
    self.assertTrue(data['success'])

  def test_model_creation(self):
    series_for_topic_dao.generate_series_for_topics()
    results = SeriesForTopic.query.all()
    import pprint
    pprint.pprint(results)
