from . import *

class EventType(Base):
  __tablename__ = 'event_types'

  id = db.Column(db.Integer, primary_key=True)
  # TODO: Integrate user model
  name = db.Column(db.String(50))
  creator = db.Column(db.String(50))
  app_id = db.Column(db.Integer, db.ForeignKey('app.id'))
  fields_info = db.Column(db.JSON)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.creator = kwargs.get('creator')
    self.fields_info = kwargs.get('fields_info')
    
