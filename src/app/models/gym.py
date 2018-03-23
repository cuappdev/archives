from . import *

class Gym(Base):
  __tablename__ = 'gyms'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False, unique=True)
  equipment = db.Column(db.String(1500))
  location = db.Column(db.String(500))
  is_gym = db.Column(db.Boolean, nullable=False, default=True)

  def __init__(self, **kwargs):
    is_gym = kwargs.get('is_gym')
    if is_gym is not None:
      self.is_gym = is_gym

    self.equipment = kwargs.get('equipment')
    self.location = kwargs.get('location')
    self.name = kwargs.get('name')

  def serialize(self):
    return {
        'id': self.id,
        'name': self.name,
        'equipment': self.equipment,
        'location': self.location
    }
