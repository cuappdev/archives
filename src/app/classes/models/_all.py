from marshmallow_sqlalchemy import ModelSchema
from app.classes.models.gym import *
from app.classes.models.gymclass import *
from app.classes.models.gymclassinstance import *
from app.classes.models.gymhour import *
from app.classes.models.instructor import *
from app.classes.models.user import *

class GymSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Gym

class GymClassSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = GymClass

class GymClassInstanceSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = GymClassInstance

class GymHourSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = GymHour

class InstructorSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Instructor

class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User
