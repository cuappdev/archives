from marshmallow_sqlalchemy import ModelSchema

from class_desc import *
from gym import *
from gymclassinstance import *
from gymhour import *
from instructor import *
from user import *

class ClassDescSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = ClassDesc

class GymSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Gym

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
