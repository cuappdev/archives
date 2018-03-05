from . import *

class Instructor(Base):
  __tablename__ = 'instructors'

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(255), nullable=False)
  last_name = db.Column(db.String(255))
  email = db.Column(db.String(255), unique=True, nullable=False)

  def __init__(self, **kwargs):
    self.first_name = kwargs.get('first_name')
    self.last_name = kwargs.get('last_name')
    self.email = kwargs.get('email')

  def serialize(self):
    return {
        'id': self.id,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'email': self.email,
    }
