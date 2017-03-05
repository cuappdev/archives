from couchbase.bucket import Bucket
from storer import Storer
import sys
import os

class CouchbaseStorer(Storer):
  """Storer of podcasts in Couchbase"""

  def __init__(self, url, password):
    """Constructor"""
    self.url      = url # Bucket URL
    print self.url
    self.password = password # Bucket password
    self.db       = Bucket(self.url, self.password) # Bucket connection

  def _dt_in_s(self, dt):
    """Datetime in seconds"""
    return int((dt-datetime.datetime(1970,1,1)).total_seconds())

  def _make_series_key(self, series_dict):
    """Series key for Couchbase"""
    return str(series_dict['id']) + ':' + str(sys.maxsize)

  def _make_episode_key(self, series_id, episode_dict):
    """Episode key for Couchbase"""
    return str(series_id) + ':' + + str(self._dt_in_s(episode_dict['pub_date']))

  def store(self, result_dict):
    """See Storer#store(result_json)"""

    # Build properly formatted bulk insert
    bulk_upsert = dict()
    series_id = result_dict['series']['id']
    bulk_upsert[self._make_series_key(result_dict['series'])] = result_dict['series']
    for e in result_dict['episodes']:
      bulk_upsert[self._make_episode_key(series_id, e)] = e

    # Bulk insert
    self.db.upsert_multi(bulk_upsert)
