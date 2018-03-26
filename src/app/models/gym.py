from . import *

class Gym(Base):
  __tablename__ = 'gyms'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False, unique=True)
  equipment = db.Column(db.String(1500))
  location = db.Column(db.String(500))
  is_gym = db.Column(db.Boolean, nullable=False, default=False)

  def __init__(self, **kwargs):
    self.equipment = kwargs.get('equipment')
    self.location = kwargs.get('location')
    self.is_gym = kwargs.get('is_gym')
    self.name = kwargs.get('name')
