from marshmallow_sqlalchemy import ModelSchema
from app.classes.models.user import *
from app.classes.models.gym import *
from app.classes.models.gymclass import *
from app.classes.models.instructor import *
from app.classes.models.gymclassinstance import *

class UserSchema(ModelSchema):
 class Meta(ModelSchema.Meta):
   model = User

class GymSchema(ModelSchema):
 class Meta(ModelSchema.Meta):
   model = Gym

class GymClassSchema(ModelSchema):
 class Meta(ModelSchema.Meta):
   model = GymClass

class InstructorSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Instructor

class GymClassInstance(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = GymClassInstance
