from marshmallow_sqlalchemy import ModelSchema
from app.events.models.user import *
from app.events.models.application import *

class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User

class ApplicationSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Application
