from sqlalchemy import UniqueConstraint
from . import *

class ClassDesc(Base):
  __tablename__ = 'class_descs'
  id = db.Column(db.Integer, primary_key=True)

  description = db.Column(db.String(2000))
  image_url = db.Column(
      db.String(1500),
      default="https://raw.githubusercontent.com/cuappdev/assets/master/fitness/classes/hiit-4.jpg",
      nullable=False
  )
  name = db.Column(db.String(300), nullable=False)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.description = kwargs.get('description')
