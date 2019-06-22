from . import *

class SongPost(Base):
  __tablename__ = 'song_posts'

  id = db.Column(db.Integer, primary_key=True)
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))
  song_id = db.Column(db.Integer, db.ForeignKey('songs.id', ondelete='CASCADE'))

  song = db.relationship('Song', cascade='all,delete')

  def __init__(self, **kwargs):
    self.post_id = kwargs.get('post_id', 0)
    self.song_id = kwargs.get('song_id', 0)
