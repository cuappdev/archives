from sqlalchemy import UniqueConstraint
from . import *

class EpisodesForTopic(Base):
  __tablename__ = 'episodes_for_topic'

  topic_id = db.Column(db.Integer, primary_key=True)
  episodes_list = db.Column(db.Text) # comma-separated

  def __init__(self, **kwargs):
    self.topic_id = kwargs.get('topic_id')
    self.episodes_list = kwargs.get('episodes_list')
