import json
from entity import Entity

class Series(Entity):
  def __init__(self, s_id, title, country, author, image_url_sm, image_url_lg, feed_url, genres):
    """
    Constructor -
    NOTE: `genres` is ';'-delimitted list of genres as a string
    """
    self.type         = 'series'
    self.id           = s_id
    self.title        = title.encode('utf-8')
    self.country      = country.encode('utf-8')
    self.author       = author.encode('utf-8')
    self.imageUrlSm   = image_url_sm.encode('utf-8')
    self.imageUrlLg   = image_url_lg.encode('utf-8')
    self.feedUrl      = feed_url.encode('utf-8')
    self.genres       = [g.encode('utf-8') for g in genres]
