from flask import json
from tests.test_case import *
from app.gyms.dao import instructors_dao as insd

class InsturctorsTestCase(TestCase):
  def setup(self):
    super(AppsTestCase, self).setUp()
    Application.query.delete()
    db_session_commit()

  def tearDown(self):
    super(AppsTestCase, self).tearDown()
    Application.query.delete()
    db_session_commit()

  def test_app_methods(self):
    
