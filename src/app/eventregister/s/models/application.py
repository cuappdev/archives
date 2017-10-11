from . import *
import hashlib
import os

class Application(Base):
  __tablename__ = 'applications'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), unique=True, nullable=False)
  secret_key = db.Column(db.String(255), unique=True, nullable=False)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.secret_key = hashlib.sha1(os.urandom(64)).hexdigest()
