from . import *

class Post(Base):
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key = True)
  like_count = db.Column(db.Integer, default = 0)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'))
  views = db.Column(db.Integer, default = 0)

  user = db.relationship('User', cascade='all,delete')
  song_posts = db.relationship('SongPost', cascade='all,delete')
  likes = db.relationship('Like', cascade='all,delete')

  def __init__(self, **kwargs):
    self.like_count = kwargs.get('like_count', 0)
    self.user_id = kwargs.get('user_id', 0)
    self.views = kwargs.get('views', 0)
