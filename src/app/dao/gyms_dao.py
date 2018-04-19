from datetime import datetime as dt
import app.dao.gymhours_dao
import app.dao.populartimeslist_dao
from . import *

def get_all_gyms():
  return Gym.query.filter(Gym.is_gym == True).all()

def get_gym_by_id(gym_id):
  return Gym.query.filter(Gym.id == gym_id).first()

def get_gym_by_name(name):
  return Gym.query.filter(Gym.name == name).first()

def get_gym_hours(gym_id):
  hours = gymhours_dao.get_gym_hour({"gym_id": gym_id})

  if hours is None:
    raise Exception('There are no gym_hours for this gym')

  return hours

def get_open_gyms(time, day_of_week):
  hours = gymhours_dao.get_gym_hour({"time": time, "day_of_week": day_of_week})
  return [h.gym for h in hours]

def serialize_gym(gym):
  serialized_gym = gym_schema.dump(gym).data
  gym_hours = gymhours_dao.get_gym_hour({'gym_id' : gym.id})
  serialized_gym_hours = []
  for gh in gym_hours:
      serialized_gh = gym_hour_schema.dump(gh)[0]
      open_time = serialized_gh['open_time']
      close_time = serialized_gh['close_time']
      serialized_gh['open_time'] = \
          (dt.strptime(open_time, '%H:%M:%S')).strftime('%I:%M%p')
      serialized_gh['close_time'] = \
          (dt.strptime(close_time, '%H:%M:%S')).strftime('%I:%M%p')
      serialized_gym_hours.append(serialized_gh)

  serialized_gym['gym_hours'] = serialized_gym_hours
  populartimeslist = \
      populartimeslist_dao.get_populartimeslist_by_gym(gym.id)
  serialized_ptl = populartimeslist_schema.dump(populartimeslist)[0]
  serialized_gym['popular_times_list'] = serialized_ptl
  return serialized_gym

def create_gym(name, equipment='', location='', image_url='', is_gym=False):
  optional_gym = Gym.query.filter(Gym.name == name).first()

  if optional_gym is not None:
    return False, optional_gym

  gym = Gym(
      equipment=equipment,
      location=location,
      image_url=image_url,
      is_gym=is_gym,
      name=name,
  )
  db_utils.commit_model(gym)
  return True, gym
