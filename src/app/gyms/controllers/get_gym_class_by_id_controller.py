from . import *
import datetime

class GetGymClassByIdController(AppDevController):

  def get_path(self):
    return '/gymclass/<id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gymclass_instance_id = request.view_args['id']
    gymclass = gymclass_dao.get_gym_class_by_id(gymclass_instance_id)
    serialized_gym = gymclass.serialize()

    return serialized_gym
