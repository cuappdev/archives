import datetime
from . import *

class GymClassInstance(Base):
  __tablename__ = 'gym_class_instances'

  id = db.Column(db.Integer, primary_key=True)
  is_cancelled = db.Column(db.Boolean, default=False)
  start_time = db.Column(db.DateTime, nullable=False)
  duration = db.Column(db.Interval, nullable=False)

  # instances can have different locations
  gym_id = db.Column(db.Integer,
                     db.ForeignKey('gyms.id', ondelete='CASCADE'))
  gym = db.relationship('Gym', backref='class_instances')

  gym_class_id = db.Column(db.Integer,
                           db.ForeignKey('gym_classes.id', ondelete='CASCADE'))
  gym_class = db.relationship('GymClass', backref='gym_classes')

  # instances can have different instructors
  instructor_id = db.Column(db.Integer,
                            db.ForeignKey('instructors.id', ondelete='CASCADE'))
  instructor = db.relationship('Instructor', backref='gym_classes')


  def __init__(self, **kwargs):
    self.duration = kwargs.get('duration')
    self.gym_id = kwargs.get('gym_id')
    self.gym_class_id = kwargs.get('gym_class_id')
    self.instructor_id = kwargs.get('instructor_id')
    self.is_cancelled = kwargs.get('is_cancelled')
    self.start_time = kwargs.get('start_time')

  def serialize(self):
    return {
        'id': self.id,
        'duration': self.duration,
        'gym': self.gym.name,
        'gym_class': self.gym_class.name,
        'instructor': self.instructor.name,
        'is_cancelled': self.is_cancelled,
        'start_time': self.start_time,
    }
