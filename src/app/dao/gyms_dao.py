import datetime
import app.dao.gymhours_dao
from . import *

def get_all_gyms():
  return Gym.query.filter(Gym.is_gym).all()

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

def create_gym(name, equipment='', location='', is_gym=False):
  optional_gym = Gym.query.filter(Gym.name == name).first()

  if optional_gym is not None:
    return False, optional_gym

  gym = Gym(
      equipment=equipment,
      location=location,
      is_gym=is_gym,
      name=name,
  )
  db_utils.commit_model(gym)
  return True, gym
