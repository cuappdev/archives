from . import *

class GetAllGymsController(AppDevController):

  def get_path(self):
    return '/gyms/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gyms = gyms_dao.get_all_gyms()
    return [gyms_dao.serialize_gym(gym) for gym in gyms]
