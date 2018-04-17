from . import *

class GetGymClassInstanceByIdController(AppDevController):

  def get_path(self):
    return '/gymclassinstance/<id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    instance = gymclassinstance_dao.get_gym_class_instance_by_id(
        request.view_args['id']
    )
    return gymclassinstance_dao.serialize_gym_class_instance(instance)
