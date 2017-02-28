import feedparser
import threading
from episode import *
import json
from copy import deepcopy
import os

class Worker(threading.Thread):

  def __init__(self, line, lock, results):
    """
    Constructor for thread that will request the RSS of a
    particular podcast series, parse the series details
    and episode information, and save the information to a
    file called `<series-id>.json`
    """
    super(Worker, self).__init__()
    self.line = line # The line detailing the series info
    self.lock = lock
    self.results = results


  def request_rss(self):
    """
    Uses information in `line` to request and return the
    RSS feed
    """
    return feedparser.parse(self.line['feed_url'])


  def build_episode(self, entry):
    """
    Build episode from entry and line info
    """
    return Episode(self.line['id'], self.line['title'], self.line['image_url'], entry)


  def run(self):
    """
    Run the task - compose full series + add to our results 
    """
    rss = self.request_rss()
    ep_jsons = []
    for entry in rss['entries']:
      ep_jsons.append(self.build_episode(entry).to_json())

    result_json = dict()
    result_json['series'] = deepcopy(self.line)
    result_json['episodes'] = ep_jsons

    self.lock.acquire()
    self.results.append(result_json)
    print("Retrieved " + self.line['id'])
    self.lock.release()
