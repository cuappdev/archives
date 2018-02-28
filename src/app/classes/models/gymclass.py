from sqlalchemy import UniqueConstraint
from . import *
from app.base import Base

class GymClass(Base):
  __tablename__ = 'gymclasses'
  __table_args__ = (
      UniqueConstraint('timestamp', 'gym_id'),
  )

  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime)
  gym_id = db.Column(db.Integer,
                            db.ForeignKey('gyms.id', ondelete='CASCADE'))

  gym = db.relationship('Gym', backref='gyms')

  def __init__(self, **kwargs):
    self.timestamp = kwargs.get('timestamp')
    self.gym_id = kwargs.get('gym_id')

  def serialize(self):
    return {
        'id': self.id,
        'gym': self.gym.name,
        'timestamp': str(self.timestamp)
    }
