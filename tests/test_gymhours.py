import datetime as dt
from flask import json
from tests.test_case import *
from app.dao import gymhours_dao as ghd
from app.dao import gyms_dao as gd

class GymHoursTestCase(TestCase):
  def setup(self):
    super(GymHoursTestCase, self).setUp()
    db_session_commit()

  def tearDown(self):
    super(GymHoursTestCase, self).tearDown()
    db_session_commit()

  def test_gymhour_methods(self):
    test_gym = gd.create_gym('test_gym1', 'test_equip', 'test_location')[1]
    test_gym2 = gd.create_gym('test_gym2', '', '')[1]
    test1 = ghd.create_gym_hour(test_gym.id, 3, dt.time(8), dt.time(23))[1]
    test2 = ghd.create_gym_hour(test_gym2.id, 2, dt.time(9), dt.time(20))[1]
    test3 = ghd.create_gym_hour(test_gym2.id, 0, dt.time(8), dt.time(19))[1]
    test4 = ghd.create_gym_hour(test_gym.id, 0, dt.time(8), dt.time(23))[1]
    self.assertEquals(test1, ghd.get_gym_hour({'id': test1.id}))
    self.assertIn(test2, ghd.get_gym_hour({'gym_id': test_gym2.id}))
    self.assertIn(test3, ghd.get_gym_hour({'gym_id': test_gym2.id}))
    self.assertEquals(test3, ghd.get_gym_hour({'gym_id': test_gym2.id, 'day_of_week':0}))
    self.assertEquals(test2, ghd.get_gym_hour({'gym_id': test_gym2.id, 'day_of_week':2}))
    self.assertIn(test4, ghd.get_gym_hour({'time': dt.time(12), 'day_of_week':0}))
    self.assertIn(test3, ghd.get_gym_hour({'time': dt.time(12), 'day_of_week':0}))
