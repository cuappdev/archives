from . import *

class Event(Base):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    event_type = db.relationship('EventType', backref='events')
    payload = db.Column(db.JSON)

    def __init__(self, **kwargs):
        self.event_type_id = kwargs.get(event_type_id)
        self.payload = kwargs.get(payload)
