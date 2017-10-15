from flask import json
from tests.test_case import *
from app import constants
from app.events.dao import users_dao

class UsersTestCase(TestCase):

  def test_user_get_methods(self):
    user1 = users_dao.get_user_by_email(constants.TEST_USER_EMAIL1)
    self.assertEquals(user1, get_user_by_id(user1.id))

  def test_user_is_registered(self):
    self.assertEquals(user_dao.is_registered(constants.TEST_USER_EMAIL1), True)
    self.assertEquals(user_dao.is_registered("invalid_email"), False)

  def test_user_verify_credentials(self):
    self.assertEquals(
        user_dao.verify_credentials(constants.TEST_USER_EMAIL,
                                    constants.TEST_USER_PASSWORD),
        True
    )
    self.assertEquals(
        user_dao.verify_credentials(constants.TEST_USER_EMAIL, "invalid_pass"),
        False
    )
