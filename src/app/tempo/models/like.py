from . import *
from sqlalchemy import UniqueConstraint

class Like(Base):
  __tablename__ = 'likes'
  __table_args__ = (
    UniqueConstraint('post_id', 'user_id'),
  )

  id = db.Column(db.Integer, primary_key = True)
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete = 'CASCADE'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'))
