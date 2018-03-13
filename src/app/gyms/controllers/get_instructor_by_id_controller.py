from . import *

class GetInstructorByIdController(AppDevController):

  def get_path(self):
    return '/instructor/<id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    instructor_id = request.view_args['id']
    instructor = instructors_dao.get_instructor_by_id(instructor_id)
    serialized_instructor = instructor.serialize()

    instructor_class = \
      gymclassinstance_dao.get_gym_class_instance_by_instructor(instructor_id)
    gymclasses = [gymclass.serialize() for gymclass in instructor_class]

    serialized_instructor["classes"] = gymclasses
    return serialized_instructor
