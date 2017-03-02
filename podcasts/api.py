import threading
import requests as r
import time

# From https://goo.gl/YzypOI
def singleton(cls):
  instances = {}
  def getinstance():
    if cls not in instances:
      instances[cls] = cls()
    return instances[cls]
  return getinstance

class API(object):

  def __init__(self):
    self.lock = threading.Lock()

  def req_itunes(self, url):
    self.lock.acquire()
    print("Requesting....")
    results = r.get(url)
    time.sleep(3.5)
    self.lock.release()
    return results

# BOOTSTRAP SINGLETON
API = singleton(API)
