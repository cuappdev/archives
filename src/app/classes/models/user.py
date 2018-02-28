from . import *
from app.base import Base

class User(Base):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), nullable=False, unique=True)
  first_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  image_url = db.Column(db.String(1500))

  def __init__(self, **kwargs):
    self.email = kwargs.get('email')
    self.first_name = kwargs.get('first_name')
    self.last_name = kwargs.get('last_name')
    self.image_url = kwargs.get('image_url')

  def serialize(self):
    return {
        'id': self.id,
        'email': self.email,
        'first_name': self.first_name,
        'last_name': self.last_name
    }
