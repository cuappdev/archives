from testcase import *

class EpisodesForUserTestCase(TestCase):

  def setUp(self):
    super(EpisodesForUserTestCase, self).setUp()
    EpisodesForUser.query.delete()
    db_session_commit()

  def test_endpoint(self):
    self.validate_model_retreival('/api/v1/episodes/user', EpisodesForUser,
                                  ['user_id', 'episodes_list'], 'episode_ids')
