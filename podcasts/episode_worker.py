import feedparser
import threading
from models.episode import Episode
import json
from copy import deepcopy
import os

class EpisodeWorker(threading.Thread):

  def __init__(self, directory, series, i):
    """
    Constructor for thread that will request the RSS of a
    particular podcast series, parse the series details
    and episode information, and save the information to a
    file called `./<directory>/<series-id>.json`
    """
    super(EpisodeWorker, self).__init__()
    self.directory = directory
    self.series    = series # All series
    self.i         = i
    # Make this ...
    if not os.path.exists('./' + self.directory):
      os.makedirs('./' + self.directory)


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

      # Write result
      with open('./' + self.directory + '/' + str(s.id) + '.json', 'wb') as outfile:
        json.dump(result_json, outfile)

      # Move onto the next one
      self.i += 10
      print("Retrieved " + str(s.id))
