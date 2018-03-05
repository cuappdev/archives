from . import *
import datetime

def get_gym_by_id(gym_id):
  return Gym.query.filter(Gym.id == gym_id).first()

def get_gym_by_name(gym_name):
  return Gym.query.filter(Gym.name == gym_name).first()

def get_gym_hours(gym_id):
  hours = gymhours_dao.get_gym_hours_by_gym_id(gym_id)

  if hours is None:
    raise Exception('gym_hours do not exist')

  return hours

def get_open_gyms(time, day_of_week):
  result = []
  for gymhour in gymhours_dao.get_gym_hours_by_day_time(time, day_of_week):
    result.append(gymhour.gym)
  return result

def create_gym(name, equipment='', location=''):
  optional_gym = get_gym_by_name(name)

  if optional_gym is not None:
    return False, optional_gym

  gym = Gym(
      name=name,
      equipment=equipment,
      location=location,
  )
  db_utils.commit_model(gym)
  return True, gym
