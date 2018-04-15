from . import *

def get_populartimeslist_by_gym(gym_id):
  return PopularTimesList.query.filter(
      PopularTimesList.gym_id == gym_id
  ).first()
