from . import *

class Song(Base):
  __tablename__ = 'songs'

  id = db.Column(db.Integer, primary_key = True)
  spotify_url = db.Column(db.String, nullable = False)
  artist = db.Column(db.String)
  track = db.Column(db.String)
  hipster_score = db.Column(db.Integer)

  def __init__(self, **kwargs):
    self.spotify_url = kwargs.get('spotify_url')
    self.artist = kwargs.get('artist')
    self.track = kwargs.get('track')
    self.hipster_score = kwargs.get('hipster_score')
