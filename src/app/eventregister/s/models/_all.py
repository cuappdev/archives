from marshmallow_sqlalchemy import ModelSchema
from app.events.models.user import *
from app.events.models.application import *
from app.events.models.event import *
from app.events.models.event_type import *

class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User

class ApplicationSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Application

class EventSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Event

class EventTypeSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = EventType
