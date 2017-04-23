from couchbase.bucket import Bucket


class Cbucket(object):
  """CouchbaseObject"""

  def __init__(self, url, password=None):
    """Constructor"""
    self.url        	= url # Bucket URL
    self.password   	= password # Bucket password
    self.bucket         = self._connect_bucket()
    self.bucket.timeout = 10

  def _connect_bucket(self):
    """Connect the DB"""
    return Bucket(self.url) if self.password is None else Bucket(self.url, password=self.password)