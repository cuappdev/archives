import unittest
import os
import sys
import random
import json

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src'
sys.path.append(src_path)

from app import app # pylint: disable=C0413
from app.podcastml.models._all import * # pylint: disable=C0413
from app.podcastml.utils.db_utils import * # pylint: disable=C0413

class TestCase(unittest.TestCase):

  def setUp(self):
    self.api_key_header = {'api_key': os.environ['API_KEY']}
    self.app = app.test_client()

  def get(self, url):
    return self.app.get(url, headers=self.api_key_header)

  def validate_model_retreival(self, base_url, model, kwarg_names, response_key,
                               num_entries=5, length_values=10):
    dummy_ids = range(1, num_entries+1)
    dummy_lists = [range(uid*length_values, (uid+1)*length_values)
                   for uid in dummy_ids]
    dummy_strings = [','.join(map(str, lst)) for lst in dummy_lists]
    dummy_entries = [model(**dict(zip(kwarg_names, [uid, lst]))) for uid, lst in
                     zip(dummy_ids, dummy_strings)]
    commit_models(dummy_entries)

    ridx = random.randint(0, num_entries-1)
    response = self.get('{}/{}/'.format(base_url, dummy_ids[ridx]))
    data = json.loads(response.data)['data']
    print(data)
    self.assertEqual(data[response_key], dummy_lists[ridx])
