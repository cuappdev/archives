from . import *

class GetInstructorByIdController(AppDevController):

  def get_path(self):
    return '/instructor/<id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    instructor_id = request.view_args['id']
    instructor_schema = InstructorSchema()
    instructor = instructors_dao.get_instructor_by_id(instructor_id)
    serialized_instructor = instructor_schema.dump(instructor).data

    instructor_class = gymclass_dao.get_gym_class_instance_by_instructor(
                instructor_id
    )
    class_descs = [class_descs_dao.get_class_desc_by_id(inc)
                   for inc in instructor_class]
    class_desc_schema = ClassDescSchema()
    gymclasses = [class_desc_schema.dump(gymclass).data
                  for gymclass in class_descs]

    serialized_instructor["classes"] = gymclasses
    return serialized_instructor
