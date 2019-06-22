from sqlalchemy import UniqueConstraint
from . import *

class EpisodesForUser(Base):
  __tablename__ = 'episodes_for_user'

  user_id = db.Column(db.Integer, primary_key=True)
  episodes_list = db.Column(db.Text) # comma-separated

  def __init__(self, **kwargs):
    self.user_id = kwargs.get('user_id')
    self.episodes_list = kwargs.get('episodes_list')
