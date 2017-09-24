from marshmallow_sqlalchemy import ModelSchema
from app.events.models.user import *
from app.events.models.app import *

class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User

class AppSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = App
