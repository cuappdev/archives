from . import *

class GetGymByIdController(AppDevController):

  def get_path(self):
    return '/gym/<gym_id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gym_id = request.view_args['gym_id']
    gym_schema = GymSchema()
    gym = gyms_dao.get_gym_by_id(gym_id)
    serialized_gym = gym_schema.dump(gym).data

    gym_hours = gymhours_dao.get_gym_hour({"gym_id": gym_id})
    gym_hour_schema = GymHourSchema()
    gym_hours = [gym_hour_schema.dump(gym_hour).data for gym_hour in gym_hours]

    serialized_gym["gym_hours"] = gym_hours
    return serialized_gym
