from . import *
import datetime

class GetClassDescByIdController(AppDevController):

  def get_path(self):
    return '/class_desc/<id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gymclass_instance_id = request.view_args['id']
    gymclass = class_descs_dao.get_class_desc_by_id(gymclass_instance_id)
    serialized_gym = gymclass.serialize()

    return serialized_gym
