from . import *

class GetGymClassByIdController(AppDevController):

  def get_path(self):
    return '/gymclass/<id>'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gymclass_id = request.view_args['id']
    gymclass = gymclass_dao.get_gym_class_by_id(gymclass_id)
    serialized_class = gymclass_schema.dump(gymclass).data
    return serialized_class
