from . import *

class GetFavoriteGymClassesController(AppDevController):

  def get_path(self):
    return '/gymclasses/favorite/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    device_id = request.args.get('device_id')
    if device_id is None:
      raise Exception('device_id is not sent')

    user = users_dao.get_user_by_device_id(device_id)
    if user is None:
      return []
    user_classes = users_dao.get_user_classes(user.id)

    serialized_classes = [gymclass_schema.dump(gc).data for gc in user_classes]
    return serialized_classes
