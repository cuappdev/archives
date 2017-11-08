import json
import os
from testcase import TestCase

class SeriesForTopicTestCase(TestCase):

  def test_endpoint(self):
    response = self.app.get('/api/v1/series/topic/hi/',
                            headers=self.api_key_header)
    data = json.loads(response.data)
    self.assertTrue(data['success'])
