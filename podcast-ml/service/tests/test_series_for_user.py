from testcase import *

class SeriesForUserTestCase(TestCase):

  def setUp(self):
    super(SeriesForUserTestCase, self).setUp()
    SeriesForUser.query.delete()
    db_session_commit()

  def test_endpoint(self):
    self.validate_model_retreival('/api/v1/series/user', SeriesForUser,
                                  ['user_id', 'series_list'], 'series_ids')
