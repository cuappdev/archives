from . import *
from sqlalchemy import UniqueConstraint

class Following(Base):
  __tablename__ = 'followings'
  __table_args__ = (
    UniqueConstraint('follower_id', 'followed_id'),
  )

  id = db.Column(db.Integer, primary_key = True)
  follower_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'))
  followed_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'))

  def __init__(self, **kwargs):
    self.follower_id = kwargs.get('follower_id', 0)
    self.followed_id = kwargs.get('followed_id', 0)
