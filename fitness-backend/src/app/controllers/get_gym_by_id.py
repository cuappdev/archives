from . import *

class GetGymByIdController(AppDevController):

  def get_path(self):
    return '/gym/<gym_id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gym_id = request.view_args['gym_id']
    gym = gyms_dao.get_gym_by_id(gym_id)
    return gyms_dao.serialize_gym(gym)
