from testcase import *

class EpisodesForTopicTestCase(TestCase):

  def setUp(self):
    super(EpisodesForTopicTestCase, self).setUp()
    EpisodesForTopic.query.delete()
    db_session_commit()

  def test_endpoint(self):
    self.validate_model_retreival('/api/v1/episodes/topic', EpisodesForTopic,
                                  ['topic_id', 'episodes_list'], 'episode_ids')
