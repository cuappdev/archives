from . import *

# define many-to-many relationship
users_to_gymclasses = db.Table('user_to_gymclasses',
                               db.Column('user_id',
                                         db.Integer,
                                         db.ForeignKey('users.id')),
                               db.Column('gymclass_id',
                                         db.Integer,
                                         db.ForeignKey('gym_classes.id'))
                               )

class User(Base):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  device_id = db.Column(db.String(255), nullable=False, unique=True)
  first_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  gym_classes = db.relationship('GymClass',
                                secondary=users_to_gymclasses,
                                backref=db.backref('users'))

  def __init__(self, **kwargs):
    self.device_id = kwargs.get('device_id')
    self.first_name = kwargs.get('first_name')
    self.last_name = kwargs.get('last_name')
