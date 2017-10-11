from sqlalchemy import UniqueConstraint
from . import *

class EventType(Base):
  __tablename__ = 'event_types'
  __table_args__ = (
      UniqueConstraint('name', 'application_id'),
  )

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  fields_info = db.Column(db.JSON)

  application = db.relationship('Application', backref='event_types')
  user = db.relationship('User', backref='event_types')

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.creator = kwargs.get('creator')
    self.application_id = kwargs.get('application_id')
    self.fields_info = kwargs.get('fields_info')
