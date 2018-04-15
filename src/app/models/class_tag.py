from . import *

# define many-to-many relationship
class_tags_to_gymclasses = db.Table(
'class_tags_to_gymclasses',
db.Column('class_tag_id', db.Integer, db.ForeignKey('class_tags.id')),
db.Column('gymclass_id', db.Integer, db.ForeignKey('gym_classes.id'))
)

class ClassTag(Base):
  __tablename__ = "class_tags"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False, unique=True)
  gym_classes = db.relationship('GymClass',
                                secondary=class_tags_to_gymclasses,
                                backref=db.backref('class_tags'))

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
