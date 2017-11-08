import unittest
import os
import sys

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src'
sys.path.append(src_path)

from app import app # pylint: disable=C0413

class TestCase(unittest.TestCase):

  def setUp(self):
    self.api_key_header = {'api_key': os.environ['API_KEY']}
    self.app = app.test_client()

  def get(self, url):
    return self.app.get(url, headers=self.api_key_header)
