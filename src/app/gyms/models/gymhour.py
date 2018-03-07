from . import *

class GymHour(Base):
  __tablename__ = 'gym_hours'

  id = db.Column(db.Integer, primary_key=True)
  gym_id = db.Column(db.Integer,
                     db.ForeignKey('gyms.id', ondelete='CASCADE'))
  gym = db.relationship('Gym', backref='gym_hours')
  day_of_week = db.Column(db.Integer, nullable=False)
  open_time = db.Column(db.Time, nullable=False)
  close_time = db.Column(db.Time, nullable=False)

  def __init__(self, **kwargs):
    self.gym_id = kwargs.get('gym_id')
    self.day_of_week = kwargs.get('day_of_week')
    self.open_time = kwargs.get('open_time')
    self.close_time = kwargs.get('close_time')

  def serialize(self):
    return {
      'id': self.id,
      'gym': self.gym.name,
      'day_of_week': self.day_of_week,
      'open_time': self.open_time,
      'close_time': self.close_time
    }
