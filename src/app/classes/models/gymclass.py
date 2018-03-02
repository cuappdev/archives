from sqlalchemy import UniqueConstraint
from . import *

class GymClass(Base):
  __tablename__ = 'gym_classes'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(300), nullable=False)
  gym_id = db.Column(db.Integer,
                     db.ForeignKey('gyms.id', ondelete='CASCADE'))

  gym = db.relationship('Gym', backref='gyms')

  description = db.Column(db.String(2000))

  instructor_id = db.Column(db.Integer,
                            db.ForeignKey('instructors.id', ondelete='CASCADE'))
  instructor = db.relationship('Instructor', backref='instructors')

  location = db.Column(db.String(500))

  def __init__(self, **kwargs):
    self.gym_id = kwargs.get('gym_id')
    self.name = kwargs.get('name')
    self.description = kwargs.get('description')
    self.instructor_id = kwargs.get('instructor_id')
    self.location = kwargs.get('location')

  def serialize(self):
    return {
        'id': self.id,
        'gym': self.gym.name,
        'name': self.name,
        'description': self.description,
        'instructor': self.instructor.first_name,
        'location': self.location
    }
