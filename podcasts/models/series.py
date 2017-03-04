import json
from entity import Entity

class Series(Entity):

  # Static (class variable, access via
  # Series.fields)
  fields = ['id', 'title', 'country', 'author', 'image_url_sm',
            'image_url_lg', 'feed_url', 'genres']


  def __init__(self, s_id, title, country, author, image_url_sm, image_url_lg, feed_url, genres):
    """
    Constructor -
    NOTE: `genres` is ';'-delimitted list of genres as a string
    """
    self.id = s_id
    self.title = title.encode('utf-8')
    self.country = country.encode('utf-8')
    self.author = author.encode('utf-8')
    self.image_url_sm = image_url_sm.encode('utf-8')
    self.image_url_lg = image_url_lg.encode('utf-8')
    self.feed_url = feed_url.encode('utf-8')
    self.genres = genres.encode('utf-8')


  def __hash__(self):
    """Series ID defines uniqueness"""
    return self.id


  @classmethod
  def from_json(cls, J):
    """Series from iTunes JSON `J`"""
    return cls(J['collectionId'], J['collectionName'], J['country'],
               J['artistName'], J['artworkUrl60'], J['artworkUrl600'],
               J['feedUrl'], ';'.join(J['genres']))


  @classmethod
  def from_line(cls, L):
    """Series from CSV line `L`"""
    return cls(L['id'], L['title'], L['country'], L['author'], L['image_url_sm'],
               L['image_url_lg'], L['feed_url'], L['genres'])


  def to_line(self):
    """To 'line' (a.k.a. array we can write with csv module)"""
    my_dict = self.__dict__
    return [my_dict[f] for f in Series.fields]
