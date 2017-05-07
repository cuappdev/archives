import threading
import requests as r
from couchbase.n1ql import N1QLQuery as NQuery

def wrapper(cls):
  instances = {}
  def getinstance():
    if cls not in instances:
      instances[cls] = cls()
    return instances[cls]
  return getinstance

class GetRequest(object):
  """Couchbase API requestor wrapper"""
  def __init__(self):
    self.lock = threading.Lock()

  def get_query(self, bucket, q,limit,offset):
    self.lock.acquire()
    query = NQuery(q + " LIMIT " + str(limit) + " OFFSET " + str(limit*offset))
    results = bucket.n1ql_query(query)
    self.lock.release()
    return results

# BOOTSTRAP SINGLETON
GetRequest = wrapper(GetRequest)
