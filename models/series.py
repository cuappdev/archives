import json

class Series(object):

  # Static (class variable, access via
  # Series.fields)
  fields = ['id', 'title', 'country', 'author', 'image_url_sm',
            'image_url_lg', 'feed_url', 'genres']

  def __init__(self, i_json):
    """Constructor from iTunes JSON `i_json`"""

    self.id = i_json['collectionId']
    self.title = i_json['collectionName']
    self.country = i_json['country']
    self.author = i_json['artistName']
    self.image_url_sm = i_json['artworkUrl60']
    self.image_url_lg = i_json['artworkUrl600']
    self.feed_url = i_json['feedUrl']
    self.genres = i_json['genres']

  def to_line(self):
    """To 'line' (a.k.a. array we can write with csv module)"""
    my_dict = self.__dict__
    return [my_dict[f] for f in Series.fields]
