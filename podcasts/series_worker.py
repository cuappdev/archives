import csv
from models.episode import Episode

class SeriesWorker(threading.Thread):

  def __init__(self, tups, i, lock, results):
    """
    Constructor - `tups` contains two-element
    tuples, containing the name of the genre,
    along with a url with podcasts related to
    that genre
    """
    self.name    = tup[0]
    self.url     = tup[1]
    self.i       = i
    self.lock    = lock # Needed to add to results
    self.results = results


  def run(self):
    """
    Requests, parses
    """
    pass 
