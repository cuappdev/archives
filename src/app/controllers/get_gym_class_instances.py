import datetime
from . import *

class GetGymClassInstancesController(AppDevController):

  def get_path(self):
    return '/gymclassinstances/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    page = request.args.get('page')
    page_size = request.args.get('page_size')

    if page_size is not None:
      gym_class_instances = gymclassinstance_dao.get_all_gym_class_instances(
          page, page_size=page_size
      )
    else:
      gym_class_instances = gymclassinstance_dao.get_all_gym_class_instances(
          page
      )

    serialized_instances = [
        gymclassinstance_dao.serialize_gym_class_instance(i) \
        for i in gym_class_instances
    ]

    return serialized_instances
