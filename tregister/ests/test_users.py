from flask import json
from tests.test_case import *
from app import constants
from app.events.dao import users_dao as ud

class UsersTestCase(TestCase):
  def test_user_get_methods(self):
    user1 = ud.get_user_by_email(constants.TEST_USER_EMAIL)
    self.assertEquals(user1, ud.get_user_by_id(user1.id))

  def test_user_is_registered(self):
    self.assertEquals(ud.is_registered(constants.TEST_USER_EMAIL), True)
    self.assertEquals(ud.is_registered("invalid_email"), False)

  def test_user_verify_credentials(self):
    self.assertEquals(
        ud.verify_credentials(constants.TEST_USER_EMAIL,
                              constants.TEST_USER_PASSWORD)[0],
        True
    )
    self.assertEquals(
        ud.verify_credentials(constants.TEST_USER_EMAIL, "invalid_pass")[0],
        False
    )
