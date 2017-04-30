from site_crawler import SiteCrawler
from series_worker import SeriesWorker

class SeriesDriver(object):
  """
  Drives the acquisition of series +
  their subsequent storage in `directory`
  """

  def __init__(self, directory):
    """Constructor"""
    self.directory = directory

  def get_series_from_urls(self, urls):
    """
    Get most popular series - `urls` = genre URLs
    """
    # Threads dispatched
    threads = []
    for i in xrange(0, 10):
      t = SeriesWorker(self.directory, urls, i)
      threads.append(t)
      t.start()

    # Get them threads together
    for t in threads:
      t.join()
