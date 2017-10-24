from flask import json
from tests.test_case import *
from app import constants
from app.events.dao import users_dao as ud
from app.events.dao import applications_dao as ad
from app.events.dao import event_types_dao as etd

class EventTypesTestCase(TestCase):
  def setUp(self):
    super(EventTypesTestCase, self).setUp()
    EventType.query.delete()
    db_session_commit()

  def test_event_types_methods(self):
    user1 = ud.get_user_by_email(constants.TEST_USER_EMAIL)
    test_app = ad.create_app("test1", user1.id)[1]
    self.assertEquals(test_app.id, ad.get_app_by_name("test1").id)
    self.assertEquals(test_app.secret_key,
                      ad.get_app_by_name("test1").secret_key)

  def test_app_is_owned_by_user(self):
    user1 = ud.get_user_by_email(constants.TEST_USER_EMAIL)
    test_app = ad.create_app("test2", user1.id)[1]
    self.assertEquals(ad.is_owned_by_user(test_app.id, user1.id), True)
