from . import *

class GetAllGymClassesController(AppDevController):

  def get_path(self):
    return '/gymclasses/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gymclasses = gymclass_dao.get_all_classes()
    serialized_classes = [gymclass_schema.dump(gc).data for gc in gymclasses]
    return serialized_classes
