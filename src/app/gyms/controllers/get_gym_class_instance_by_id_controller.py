from . import *

class GetGymClassInstanceByIdController(AppDevController):

  def get_path(self):
    return '/gymclassinstance/<id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gymclass_instance_id = request.view_args['id']
    gymclass_instance = \
        gymclassinstance_dao.get_gym_class_instance_by_id(gymclass_instance_id)
    serialized_gym = gymclass_instance.serialize()

    # get instructor
    instructor = \
        instructors_dao.get_instructor_by_id(gymclass_instance.instructor_id)
    instructor = instructor.serialize()
    serialized_gym["instructor"] = instructor

    # get gymclass
    gymclass = gymclass_dao.get_gym_class_by_id(gymclass_instance.gym_class_id)
    gymclass = gymclass.serialize()
    serialized_gym["gym_class"] = gymclass

    return serialized_gym
