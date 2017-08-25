from . import *

class SpotifyCred(Base):
  __tablename__ = 'spotify_creds'

  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'))
  access_token = db.Column(db.String, nullable = False)
  refresh_token = db.Column(db.String, nullable = False)
  expires_at = db.Column(db.String, nullable = False)
  spotify_id = db.Column(db.String)
  playlist_id = db.Column(db.String)

  def __init__(self, **kwargs):
    self.user_id = kwargs.get('user_id')
    self.access_token = kwargs.get('access_token')
    self.refresh_token = kwargs.get('refresh_token')
    self.expires_at = kwargs.get('expires_at')
    self.spotify_id = kwargs.get('spotify_id', None)
    self.playlist_id = kwargs.get('playlist_id', None)
