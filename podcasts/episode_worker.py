import feedparser
import threading
from models.episode import Episode
from copy import deepcopy
import os

class EpisodeWorker(threading.Thread):

  def __init__(self, storer, series, i):
    """
    Constructor for thread that will request the RSS of a
    particular podcast series, parse the series details
    and episode information, and save the information
    w/`storer`
    """
    super(EpisodeWorker, self).__init__()
    self.storer = storer
    self.series = series # All series
    self.i      = i


  def request_rss(self, url):
    """
    Uses information in `line` to request and return the
    RSS feed
    """
    return feedparser.parse(url)


  def run(self):
    """
    Run the task - compose full series + add to our results
    """
    while self.i < len(self.series):
      # Grab line + RSS
      s = self.series[self.i]
      rss = self.request_rss(s.feed_url)

      # Compose Episodes
      ep_jsons = []
      for entry in rss['entries']:
        ep_jsons.append(Episode(s, entry).to_json())

      # Build result JSON
      result_json = dict()
      result_json['series'] = deepcopy(s.__dict__)
      result_json['series']['genres'] = \
        result_json['series']['genres'].split(';')
      result_json['episodes'] = ep_jsons

      # Store podcast
      self.storer.store(result_json)

      # Move onto the next one
      self.i += 20
      print("Retrieved " + str(s.id))
