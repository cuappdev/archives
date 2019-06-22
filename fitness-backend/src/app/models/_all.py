from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from app.models.class_desc import *
from app.models.class_tag import *
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
    exclude = ('created_at', 'updated_at')

class ClassTagSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = ClassTag
    exclude = ('created_at', 'updated_at')

class GymSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Gym
    exclude = ('created_at', 'updated_at')

class GymClassSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = GymClass
    exclude = ('created_at', 'updated_at')

class GymClassInstanceSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = GymClassInstance
    exclude = ('created_at', 'updated_at')

class GymHourSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = GymHour
    exclude = ('created_at', 'updated_at', 'gym')

class InstructorSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Instructor
    exclude = ('created_at', 'updated_at')

class PopularTimesListSchema(ModelSchema):
  monday = fields.Function(lambda obj: eval(obj.monday))
  tuesday = fields.Function(lambda obj: eval(obj.tuesday))
  wednesday = fields.Function(lambda obj: eval(obj.wednesday))
  thursday = fields.Function(lambda obj: eval(obj.thursday))
  friday = fields.Function(lambda obj: eval(obj.friday))
  saturday = fields.Function(lambda obj: eval(obj.saturday))
  sunday = fields.Function(lambda obj: eval(obj.sunday))
  class Meta(ModelSchema.Meta):
    model = PopularTimesList
    exclude = ('created_at', 'updated_at', 'gym')

class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User
    exclude = ('created_at', 'updated_at')

# Serializers
class_tag_schema = ClassTagSchema()
gym_schema = GymSchema()
gymclass_schema = GymClassSchema()
gymclassinstance_schema = GymClassInstanceSchema()
instructor_schema = InstructorSchema()
class_desc_schema = ClassDescSchema()
gym_hour_schema = GymHourSchema()
user_schema = UserSchema()
populartimeslist_schema = PopularTimesListSchema()
