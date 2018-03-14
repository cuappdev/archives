from . import *
import datetime

class GetAllGymClassInstancesController(AppDevController):

  def get_path(self):
    return '/gymclassinstances/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gymclass_instances = gymclassinstance_dao.get_all_gym_class_instances()
    serialized_gyms = [gymclass_instance.serialize() for gymclass_instance in gymclass_instances]

    #get instructor
    # instructor = instructors_dao.get_instructor_by_id(gymclass_instance.instructor_id)
    # instructor = instructor.serialize()
    # serialized_gym["instructor"] = instructor
    #
    # #get gymclass
    # gymclass = gymclass_dao.get_gym_class_by_id(gymclass_instance.gym_class_id)
    # gymclass = gymclass.serialize()
    # serialized_gym["gym_class"] = gymclass

    return serialized_gyms
