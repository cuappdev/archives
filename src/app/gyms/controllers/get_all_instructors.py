from . import *

class GetAllInstructorsController(AppDevController):
  def get_path(self):
    return '/instructors/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    instructors = intructors_dao.get_all_instructors()
    return [(instructor.id, instructor.first_name)
            for instructor in instructors]
