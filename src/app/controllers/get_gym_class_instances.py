import datetime
from . import *

class GetGymClassInstancesController(AppDevController):

  def get_path(self):
    return '/gymclassinstances/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    page = request.headers.get('page')
    gymclass_instances = \
        gymclassinstance_dao.get_all_gym_class_instances(page)
    serialized_gyms = []
    for gymclass_instance in gymclass_instances:
        serialized_gym = {"id": gymclass_instance.id}

        gym_class = gymclass_dao.get_gym_class_by_id(
                gymclass_instance.gym_class_id
        )

        # get instructor
        instructor = instructors_dao.get_instructor_by_id(
                gym_class.instructor_id
        )
        instructor = instructor_schema.dump(instructor).data
        serialized_gym["instructor"] = instructor

        # get class_descj
        class_desc = class_descs_dao.get_class_desc_by_id(
                gym_class.class_desc_id
        )
        class_desc = class_desc_schema.dump(class_desc).data
        serialized_gym["class_desc"] = class_desc

        serialized_gyms.append(serialized_gym)

    return serialized_gyms
