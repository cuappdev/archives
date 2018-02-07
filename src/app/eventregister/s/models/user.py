import datetime
import hashlib
import os
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
  session_token = db.Column(db.String(255), nullable=False, unique=True)
  session_expiration = db.Column(db.DateTime, nullable=False)
  update_token = db.Column(db.String(255), nullable=False, unique=True)
  applications = db.relationship('Application',
                                 secondary=users_to_applications,
                                 backref=db.backref('users'))

  def __init__(self, **kwargs):
    self.email = kwargs.get('email')
    self.password_digest = bcrypt.hashpw(kwargs.get('password').encode('utf8'),
                                         bcrypt.gensalt(rounds=13))
    self.first_name = kwargs.get('first_name')
    self.last_name = kwargs.get('last_name')
    self.renew_session()

  def serialize(self):
    return {
        'id': self.id,
        'email': self.email,
        'first_name': self.first_name,
        'last_name': self.last_name
    }

  def verify_password(self, password):
    return bcrypt.checkpw(password.encode('utf8'),
                          self.password_digest.encode('utf8'))

  def _urlsafe_base_64(self):
    return hashlib.sha1(os.urandom(64)).hexdigest()

  def renew_session(self):
    self.session_token = self._urlsafe_base_64()
    self.session_expiration = datetime.datetime.now() + \
                              datetime.timedelta(days=1)
    self.update_token = self._urlsafe_base_64()

  def verify_session_token(self, session_token):
    return session_token == self.session_token and \
      datetime.datetime.now() < self.session_expiration

  def verify_update_token(self, update_token):
    return update_token == self.update_token
