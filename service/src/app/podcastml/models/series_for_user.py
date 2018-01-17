from sqlalchemy import UniqueConstraint
from . import *

class SeriesForUser(Base):
  __tablename__ = 'series_for_user'

  user_id = db.Column(db.Integer, primary_key=True)
  series_list = db.Column(db.Text) # comma-separated

  def __init__(self, **kwargs):
    self.user_id = kwargs.get('user_id')
    self.series_list = kwargs.get('series_list')
