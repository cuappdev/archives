from . import *

class GetAllGymsController(AppDevController):

  def get_path(self):
    return '/gyms/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gyms = gyms_dao.get_all_gyms()
    result = []
    for gym in gyms:
        serialized_gym = gym_schema.dump(gym).data
        gym_hours = gymhours_dao.get_gym_hour({'gym_id' : gym.id})
        serialized_gym_hours = [gym_hour_schema.dump(gh) for gh in gym_hours]
        serialized_gym['gym_hours'] = serialized_gym_hours
        populartimeslist = \
            populartimeslist_dao.get_populartimeslist_by_gym(gym.id)
        serialized_ptl = populartimeslist_schema.dump(populartimeslist)
        serialized_gym['popular_times_list'] = serialized_ptl
        result.append(serialized_gym)
    return result
