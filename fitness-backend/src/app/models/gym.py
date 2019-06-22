from . import *

class Gym(Base):
  __tablename__ = 'gyms'
  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(255), nullable=False, unique=True)
  equipment = db.Column(db.String(1500))
  image_url = db.Column(db.String(1500), default="")
  is_gym = db.Column(db.Boolean, nullable=False, default=False)

  location_gym_id = db.Column(
      db.Integer,
      db.ForeignKey('gyms.id', ondelete='CASCADE')
  )
  location_gym = db.relationship('Gym', remote_side=[id])

  def __init__(self, **kwargs):
    self.equipment = kwargs.get('equipment')
    self.image_url = kwargs.get('image_url')
    self.is_gym = kwargs.get('is_gym')
    self.location_id = kwargs.get('location_gym_id')
    self.name = kwargs.get('name')
