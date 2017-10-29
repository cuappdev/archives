from flask import json
from tests.test_case import *
from app import constants
from app.events.dao import users_dao as ud
from app.events.dao import applications_dao as ad
from app.events.dao import event_types_dao as etd
from app.events.dao import event_dao as ed

class EventsTestCase(TestCase):
  def setUp(self):
    super(EventsTestCase, self).setUp()
    Application.query.delete() # event-types should be cascade-deleted
    user1 = ud.get_user_by_email(constants.TEST_USER_EMAIL)
    test_app = ad.create_app("app1", user1.id)[1]
    fields_info = {
        "ex1": {"type": "str", "required": False, "default": "hello"}
    }
    test_event_type = etd.create_event_type( # testing valid event
        test_app.id,
        "test_event_type",
        test_user.id,
        fields_info
    )
    db_session_commit()
    commit_model(test_app)
    commit_model(test_event_type)

  def test_event_creation(self):
    pass
