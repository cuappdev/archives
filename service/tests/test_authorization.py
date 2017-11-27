import json
import os
from testcase import TestCase

class AuthorizeTestCase(TestCase):

  def test_no_api_key(self):
    response = self.app.get('/api/v1/series/topic/hi/')
    data = json.loads(response.data)
    self.assertFalse(data['success'])

  def test_wrong_api_key(self):
    wrong_api_key_header = {'api_key': 'some_wrong_key'}
    response = self.app.get('/api/v1/series/topic/hi/',
                            headers=wrong_api_key_header)
    data = json.loads(response.data)
    self.assertFalse(data['success'])

  def test_correct_api_key(self):
    response = self.get('/api/v1/series/topic/hi/')
    data = json.loads(response.data)
    self.assertTrue(data['success'])
