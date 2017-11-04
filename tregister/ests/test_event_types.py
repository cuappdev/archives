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
