from . import *

class GymClass(Base):
  __tablename__ = "gym_classes"

  id = db.Column(db.Integer, primary_key=True)

  class_desc_id = db.Column(
      db.Integer,
      db.ForeignKey('class_descs.id', ondelete='CASCADE')
  )
  class_desc = db.relationship('ClassDesc', backref='gym_classes')

  instructor_id = db.Column(
      db.Integer,
      db.ForeignKey('instructors.id', ondelete='CASCADE')
  )
  instructor = db.relationship('Instructor', backref='gym_classes')

  def __init__(self, **kwargs):
    self.class_desc_id = kwargs.get('class_desc_id')
    self.instructor_id = kwargs.get('instructor_id')
