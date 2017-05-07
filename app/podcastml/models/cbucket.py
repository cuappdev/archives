#### Couchbase Imports
from couchbase.bucket import Bucket
####
#### Model Imports
from app.podcastml.models.getrequest import GetRequest
from app.podcastml.models.series import Series
from app.podcastml.models.episode import Episode
####
#### Import Logger
import log
####

class Cbucket(object):
  """
    CouchbaseObject
  """
  def __init__(self, url, password=None):
    """
      Constructor
    """
    self.url        	   = url # Bucket URL
    self.password   	   = password # Bucket password
    self.bucket          = self._connect_bucket() # Connect the DB
    self.bucket.timeout  = 10 # Timeafter which you should timeout
    self.logger          = log.logger

  def _connect_bucket(self):
    """
      Connect the DB
    """
    return Bucket(self.url) if self.password is None else Bucket(self.url, password=self.password)

  def get_episodes(self,series_dict={},limit=100):
    """
      This method is responsible for getting episodes from the Couchbase bucket called podcasts

      @param series_dict: series dictionary used to bind episodes to series
      @param limit: Limit of how many values to request. Initialized to 100

      @return: dictionary of episodes
    """
    episodes = {}
    offset = 0
    series_keys = series_dict.keys()
    while True:
      self.logger.info('Grabbing %d th episode' % (limit*offset) )
      result = GetRequest().get_query(self.bucket,"select * from podcasts WHERE type=\"episode\"",limit,offset)
      if result.get_single_result() == None:
        break
      for row in result:
        r = row['podcasts']
        if r['seriesId'] in series_keys:
          episodes[r['title'].encode('ascii','ignore')] = Episode(series_dict[r['seriesId']],r['title'],r['author'],r['summary'],r['pubDate'],r['duration'],[t.encode('ascii','ignore').replace("\"","") for t in r['tags']],r['audioUrl'])
      offset+=1
    return episodes

  def get_series(self,limit=100):
    """
      This method is responsible for getting series from the Couchbase bucket

      @param limit: Limit of how many values to request. Initialized to 100

      @return: dictionary of series
    """
    series_dict = {}
    offset = 0
    while True:
      self.logger.info('Grabbing %d th series' % (limit*offset) )
      result = GetRequest().get_query(self.bucket,"select * from podcasts WHERE type=\"series\"",limit,offset)
      if result.get_single_result() == None:
        break
      for row in result:
        r = row['podcasts']
        series_dict[int(r['id'])] = Series(r['id'], r['author'], r['country'], r['author'], r['imageUrlSm'], r['imageUrlLg'], r['feedUrl'], r['genres'])
      offset+=1
    return series_dict
