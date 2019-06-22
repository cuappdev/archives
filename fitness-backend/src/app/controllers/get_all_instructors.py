from . import *

class GetAllInstructorsController(AppDevController):
  def get_path(self):
    return '/instructors/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    instructors = instructors_dao.get_all_instructors()
    result = []
    for instructor in instructors:
        serialized_instructor = instructor_schema.dump(instructor).data

        instructor_class = gymclass_dao.get_gym_classes_by_instructor(
                    instructor.id
        )
        class_descs = [class_descs_dao.get_class_desc_by_id(inc.id)
                       for inc in instructor_class]
        gymclasses = [class_desc_schema.dump(gymclass).data
                      for gymclass in class_descs]

        serialized_instructor["classes"] = gymclasses
        result.append(serialized_instructor)
    return result
