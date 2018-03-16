from . import *
import datetime

class GetAllGymClassInstancesController(AppDevController):

  def get_path(self):
    return '/gymclassinstances/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    page = request.headers.get('page')
    gymclass_instances = \
        gymclassinstance_dao.get_all_gym_class_instances(page)
    serialized_gyms = []
    for gymclass_instance in gymclass_instances.items:
        serialized_gym = gymclass_instance.serialize()

        # get instructor
        instructor = \
            instructors_dao.get_instructor_by_id(gymclass_instance.instructor_id)
        instructor = instructor.serialize()
        serialized_gym["instructor"] = instructor

        # get gymclass
        gymclass = \
            gymclass_dao.get_gym_class_by_id(gymclass_instance.gym_class_id)
        gymclass = gymclass.serialize()
        serialized_gym["gym_class"] = gymclass

        serialized_gyms.append(serialized_gym)

    return serialized_gyms
