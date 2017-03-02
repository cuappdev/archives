import threading
import csv
from models.series import Series
from series_crawler import SeriesCrawler
import os

class SeriesWorker(threading.Thread):

  def __init__(self, tups, i):
    """
    Constructor - `tups` contains two-element
    tuples, containing the name of the genre,
    along with a url with podcasts related to
    that genre
    """
    super(SeriesWorker, self).__init__()
    self.tups    = tups
    self.i       = i
    self.crawler = SeriesCrawler()
    # Make this ...
    if not os.path.exists('./csv'):
      os.makedirs('./csv')

  def run(self):
    """Requests, parses series, writes to appropriate CSV"""

    while self.i < len(self.tups):
      name = self.tups[self.i][0]
      url  = self.tups[self.i][1]
      self.crawler.set_url(url)
      series = self.crawler.get_series()
      writer = csv.writer(open('./csv/' + name + '.csv', 'wb'))
      writer.writerow(Series.fields)
      for s in series:
        writer.writerow(s.to_line())
      self.i += 10
      print("Got in " + name)
