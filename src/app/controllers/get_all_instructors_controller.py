from . import *

class GetAllInstructorsController(AppDevController):
  def get_path(self):
    return '/instructors/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    instructors = instructors_dao.get_all_instructors()
    return [(instructor.id, instructor.name) for instructor in instructors]
