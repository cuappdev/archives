from . import *

class Instructor(Base):
  __tablename__ = 'instructors'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')

  def serialize(self):
    return {
        'id': self.id,
        'name': self.name
    }
