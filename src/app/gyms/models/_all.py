from marshmallow_sqlalchemy import ModelSchema
from app.gyms.models.gym import *
from app.gyms.models.gymclass import *
from app.gyms.models.gymclassinstance import *
from app.gyms.models.gymhour import *
from app.gyms.models.instructor import *
from app.gyms.models.user import *

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
