import requests as r
import constants as c
from lxml import html
from models.series import Series
import time
import urllib

# SeriesCrawler, to get series from a particular webpage
class SeriesCrawler(object):

  def __init__(self, url):
    """Constructor"""
    self.url    = url
    self.ids    = []
    self.series = []


  def _e_to_id(self, e):
    """
    Private - Convert HTML element `e`'s
    'href' attribute to a series id
    """
    return (e.attrib['href']
                    [(e.attrib['href']
                    .rfind('/id')+3):]
                    .replace('?mt=2', ''))


  def get_ids(self):
    """Grab the ID's of podcasts on `self.url` page"""
    page = r.get(self.url)
    tree = html.fromstring(page.content)
    ids_elements = tree.xpath("//div[@id='selectedcontent']/div/ul/li/a")
    return [self._e_to_id(e) for e in ids_elements]


  def get_series(self):
    """
    Grab all series from a `self.url`, based on
    id acquisition
    """
    ids = self.get_ids()
    i = 0; j = 100
    while i < len(ids):
      curr_ids = ids[i:j]
      ids_with_coms = ','.join(curr_ids)
      id_param = { 'id': ids_with_coms }
      results = r.get(c.ITUNES_LOOKUP_URL + urllib.urlencode(id_param)).json()['results']
      self.series.extend(results)
      i += 100; j += 100
      time.sleep(3.5)
    return [Series(j).to_line() for j in self.series]
