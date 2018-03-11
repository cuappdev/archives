from sqlalchemy import UniqueConstraint
from . import *

class GymClass(Base):
  __tablename__ = 'gym_classes'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(300), nullable=False)
  description = db.Column(db.String(2000))

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.description = kwargs.get('description')

  def serialize(self):
    return {
        'id': self.id,
        'name': self.name,
        'gym': self.gym.name,
        'description': self.description,
    }
