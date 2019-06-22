from sqlalchemy import UniqueConstraint
from . import *

class Event(Base):
  __tablename__ = 'events'
  # __table_args__ = (
  #     UniqueConstraint('timestamp', 'event_type_id'),
  # )

  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime)
  event_type_id = db.Column(db.Integer,
                            db.ForeignKey('event_types.id', ondelete='CASCADE'))
  payload = db.Column(db.JSON)

  event_type = db.relationship('EventType', backref='events')

  def __init__(self, **kwargs):
    self.timestamp = kwargs.get('timestamp')
    self.event_type_id = kwargs.get('event_type_id')
    self.payload = kwargs.get('payload')

  def serialize(self):
    return {
        'id': self.id,
        'event_type': self.event_type.name,
        'payload': self.payload,
        'timestamp': str(self.timestamp)
    }