from podcasts.site_crawler import SiteCrawler
from podcasts.series_worker import SeriesWorker

class SeriesDriver(object):

  def get_popular(self):
    """Get most popular series"""

    # Grab appropriate info
    tups = SiteCrawler().get_genres()

    # Threads dispatched
    threads = []
    for i in xrange(0, 10):
      t = SeriesWorker(tups, i)
      threads.append(t)
      t.start()

    # Get them threads together
    for t in threads:
      t.join()


# Run this
SeriesDriver().get_popular()
