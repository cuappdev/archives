from . import *
import datetime

class GetAllGymClassesController(AppDevController):

  def get_path(self):
    return '/gymclasses/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gymclasses = gymclass_dao.get_all_gym_classes()
    serialized_gyms = [gymclass.serialize() for gymclass in gymclasses]

    return serialized_gyms
