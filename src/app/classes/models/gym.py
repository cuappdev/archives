from . import *

class Gym(Base):
  __tablename__ = 'gyms'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False, unique=True)
  equipment = db.Column(db.String(1500))
  location = db.Column(db.String(500))

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.equipment = kwargs.get('equipment')
    self.location = kwargs.get('location')

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'equipment': self.equipment,
      'location': self.location
    }
