import datetime
from . import *

class GymClassInstance(Base):
  __tablename__ = 'gym_class_instances'

  id = db.Column(db.Integer, primary_key=True)
  is_cancelled = db.Column(db.Boolean, default=False)
  start_time = db.Column(db.DateTime, nullable=False)
  duration = db.Column(db.Interval, nullable=False)

  gym_class_id = db.Column(db.Integer,
                           db.ForeignKey('gym_classes.id', ondelete='CASCADE'))
  gym_class = db.relationship('GymClass', backref='gym_classes')

  def __init__(self, **kwargs):
    self.is_cancelled = kwargs.get('is_cancelled')
    self.start_time = kwargs.get('start_time')
    self.duration = kwargs.get('duration')
    self.gym_class_id = kwargs.get('gym_class_id')

  def serialize(self):
    return {
        'id': self.id,
        'is_cancelled': self.is_cancelled,
        'start_time': self.start_time,
        'duration': self.duration,
        'gym_class': self.gym_class.name
    }
