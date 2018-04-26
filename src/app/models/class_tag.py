from . import *

# define many-to-many relationship
class_tags_to_class_descs = db.Table(
'class_tags_to_class_descs',
db.Column('class_tag_id', db.Integer, db.ForeignKey('class_tags.id')),
db.Column('class_desc_id', db.Integer, db.ForeignKey('class_descs.id'))
)

class ClassTag(Base):
  __tablename__ = "class_tags"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False, unique=True)
  image_url = db.Column(db.String(255), nullable=False,
    default="https://github.com/cuappdev/assets/blob/master/fitness/class_tags/cardio.png")
  class_descs = db.relationship('ClassDesc',
                                secondary=class_tags_to_class_descs,
                                backref=db.backref('class_tags'))

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
