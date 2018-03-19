import datetime as dt
from flask import json
from tests.test_case import *
from app.dao import gyms_dao as gd
from app.dao import gymhours_dao as ghd

class GymsTestCase(TestCase):
  def setup(self):
    super(GymsTestCase, self).setUp()
    db_session_commit()

  def tearDown(self):
    super(GymsTestCase, self).tearDown()
    db_session_commit()

  def test_gym_methods(self):
    test_gym = gd.create_gym('test_gym1', 'test_equip', 'test_location')[1]
    self.assertEquals(test_gym.id, gd.get_gym_by_name('test_gym1').id)
    self.assertEquals('test_gym1', gd.get_gym_by_id(test_gym.id).name)
    test_gym2 = gd.create_gym('test_gym2', '', '')[1]
    all_gyms = gd.get_all_gyms()
    self.assertIn(test_gym, all_gyms)
    self.assertIn(test_gym2, all_gyms)
    # tests for hours
    test_hour = ghd.create_gym_hour(test_gym.id, 1, dt.time(9), dt.time(21))[1]
    self.assertIn(test_hour, gd.get_gym_hours(test_gym.id))
    self.assertIn(test_gym, gd.get_open_gyms(dt.time(10), 1))
    self.assertNotIn(test_gym, gd.get_open_gyms(dt.time(22), 1))
    self.assertNotIn(test_gym, gd.get_open_gyms(dt.time(10), 4))
