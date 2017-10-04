import bcrypt
from . import *

# define many-to-many relationship
users_to_applications = db.Table('user_to_applications',
                                 db.Column('user_id',
                                           db.Integer,
                                           db.ForeignKey('users.id')),
                                 db.Column('application_id',
                                           db.Integer,
                                           db.ForeignKey('applications.id'))
                                )

class User(Base):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), nullable=False, unique=True)
  password_digest = db.Column(db.Text, nullable=False)
  first_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  applications = db.relationship('Application',
                                 secondary=users_to_applications,
                                 backref=db.backref('users'))

  def __init__(self, **kwargs):
    self.email = kwargs.get('email')
    self.password_digest = bcrypt.hashpw(kwargs.get('password').encode('utf8'),
                                         bcrypt.gensalt())
    self.first_name = kwargs.get('first_name')
    self.last_name = kwargs.get('last_name')

  def verify_password(self, password):
    return bcrypt.checkpw(password.encode('utf8'), self.password_digest.encode('utf8'))
