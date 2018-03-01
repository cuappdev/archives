from sqlalchemy import UniqueConstraint
from . import *

class GymClass(Base):
  __tablename__ = 'gym_classes'

  id = db.Column(db.Integer, primary_key=True)
  gym_id = db.Column(db.Integer,
                     db.ForeignKey('gyms.id', ondelete='CASCADE'))

  gym = db.relationship('Gym', backref='gyms')
  description = db.Column(db.String(2000))

  def __init__(self, **kwargs):
    self.gym_id = kwargs.get('gym_id')
    self.description = kwargs.get('description')

  def serialize(self):
    return {
        'id': self.id,
        'gym': self.gym.name,
        'description': self.description
    }
