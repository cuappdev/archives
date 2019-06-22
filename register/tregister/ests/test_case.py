import unittest
import os
import sys

from tests.loading_utils import *

class TestCase(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()
    load_users()

  def tearDown(self):
    ud.clear_all_apps()
    db_session_commit()
