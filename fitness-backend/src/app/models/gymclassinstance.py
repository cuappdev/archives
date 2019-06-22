import datetime
from . import *

class GymClassInstance(Base):
  __tablename__ = 'gym_class_instances'

  id = db.Column(db.Integer, primary_key=True)
  is_cancelled = db.Column(db.Boolean, default=False)
  start_dt = db.Column(db.DateTime, nullable=True)
  duration = db.Column(db.Interval, nullable=True)

  # instances can have different locations
  gym_id = db.Column(db.Integer,
                     db.ForeignKey('gyms.id', ondelete='CASCADE'))
  gym = db.relationship('Gym', backref='class_instances')

  gym_class_id = db.Column(db.Integer,
                           db.ForeignKey('gym_classes.id', ondelete='CASCADE'))
  gym_class = db.relationship('GymClass', backref='gym_class_instances')

  def __init__(self, **kwargs):
    self.duration = kwargs.get('duration')
    self.gym_id = kwargs.get('gym_id')
    self.class_desc_id = kwargs.get('class_desc_id')
    self.gym_class_id = kwargs.get('gym_class_id')
    self.is_cancelled = kwargs.get('is_cancelled')
    self.start_dt = kwargs.get('start_dt')
