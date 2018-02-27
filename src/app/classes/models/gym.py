from . import *

class Gym(Base):
  __tablename__ = 'gyms'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False, unique=True)
  hours = db.Column(db.String(1500))
  equip = db.Column(db.String(1500))
  loc = db.Column(db.String(500))

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.hours = kwargs.get('hours')
    self.equip = kwargs.get('equip')
    self.loc = kwargs.get('loc')

def serialize(self):
  return {
      'id': self.id,
      'name': self.name,
      'hours': self.hours,
      'equip': self.equip,
      'loc': self.loc
  }
