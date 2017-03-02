import threading
from podcasts.site_crawler import SiteCrawler
from podcasts.series_crawler import SeriesCrawler

class SeriesDriver(object):

  def get_popular(self):
    """Get most popular series"""
    # Straight up links
    site_c = SiteCrawler().get_genres()
    
