import json
import os
from testcase import *
from app.podcastml.dao import series_for_topic_dao

class SeriesForTopicTestCase(TestCase):

  def setUp(self):
    super(SeriesForTopicTestCase, self).setUp()
    SeriesForTopic.query.delete()
    db_session_commit()

  def test_model_creation(self):
    series_for_topic_dao.generate_series_for_topics()
    self.assertTrue(SeriesForTopic.query.count() > 0)
