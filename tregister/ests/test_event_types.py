from flask import json
from tests.test_case import *
from app import constants
from app.events.dao import users_dao as ud
from app.events.dao import applications_dao as ad
from app.events.dao import event_types_dao as etd

class EventTypesTestCase(TestCase):
  def setUp(self):
    super(EventTypesTestCase, self).setUp()
    Application.query.delete() # event-types should be cascade-deleted
    user1 = ud.get_user_by_email(constants.TEST_USER_EMAIL)
    test_app = ad.create_app("app1", user1.id)[1]
    db_session_commit()
    commit_model(test_app)

  def tearDown(self):
    super(EventTypesTestCase, self).tearDown()
    Application.query.delete()
    db_session_commit()

  def test_event_type_creation(self):
    test_user = ud.get_user_by_email(constants.TEST_USER_EMAIL)
    test_app = ad.get_app_by_name("app1")
    fields_info = {
        "ex1": {"type": "str", "required": False, "default": u"hello"}
    }
    etd.create_event_type( # testing valid event
        test_app.id,
        "test_event_type",
        fields_info
    )
    with self.assertRaises(Exception):
      fields_info = {
          "ex1": {"type": "Str", "required": False, "default": 5}
      }
      etd.create_event_type( # testing invalid event
          test_app.id,
          "test_incorrect_event",
          fields_info
      )
    with self.assertRaises(Exception):
      fields_info = {
          "ex1": {"type": "str", "required": 5, "default": 5}
      }
      etd.create_event_type( # testing invalid event
          test_app.id,
          "test_incorrect_event",
          fields_info
      )
    with self.assertRaises(Exception):
      fields_info = {
          "ex1": {"type": "str", "required": False, "default": 5}
      }
      etd.create_event_type( # testing invalid event
          test_app.id,
          "test_incorrect_event",
          fields_info
      )
