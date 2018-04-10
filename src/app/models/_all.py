from marshmallow_sqlalchemy import ModelSchema

from app.models.class_desc import *
from app.models.gym import *
from app.models.gymclass import *
from app.models.gymclassinstance import *
from app.models.gymhour import *
from app.models.instructor import *
from app.models.populartimeslist import *
from app.models.user import *

class ClassDescSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = ClassDesc

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

class PopularTimesListSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = PopularTimesList

class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User
