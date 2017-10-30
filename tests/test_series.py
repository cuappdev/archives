import sys
import json
from tests.test_case import *
from app.pcasts.dao import series_dao, subscriptions_dao
from app import constants # pylint: disable=C0413

class SeriesTestCase(TestCase):

  def setUp(self):
    super(SeriesTestCase, self).setUp()
    Subscription.query.delete()
    series_dao.clear_all_subscriber_counts()
    db_session_commit()

  def tearDown(self):
    # Make sure all subscriptions are cleared
    super(SeriesTestCase, self).tearDown()
    Subscription.query.delete()
    db_session_commit()

  def test_get_series_by_id(self):
    user = User.query \
       .filter(User.google_id == constants.TEST_USER_GOOGLE_ID1).first()
    series_id = '1211520413'
    response = self.app.get('api/v1/series/{}/'.format(series_id))
    result = json.loads(response.data)['data']['series']
    expected_series = series_dao.get_series(series_id, user.id)
    self.assertEqual(result['id'], expected_series.id)

  def test_discover_series(self):
    series_id1 = '1211520413'
    self.app.post('api/v1/subscriptions/{}/'.format(series_id1))
    response = \
      self.app.get('api/v1/discover/series/?offset={}&max={}'.format(0, 2))
    series_results = json.loads(response.data)['data']['series']
    self.assertEquals(int(series_id1), series_results[0]['id'])
