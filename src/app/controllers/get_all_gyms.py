from . import *

class GetAllGymsController(AppDevController):

  def get_path(self):
    return '/gyms/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gyms = gyms_dao.get_all_gyms()
    gym_schema = GymSchema()
    serialized_gyms = [gym_schema.dump(gym).data for gym in gyms]
    return serialized_gyms
