from . import *
import datetime

def get_gym_hour_by_id(gym_hours_id):
  return GymHour.query.filter(GymHour.id == gym_hours_id).first()

def get_gym_hour_by_day_of_week(gym_id, day_of_week):
  return GymHour.query.filter(GymHour.gym_id == gym_id,
                              GymHour.day_of_week == day_of_week).first()

def get_gym_hours_by_gym_id(gym_id):
  return GymHour.query.filter(GymHour.gym_id == gym_id).all()

def get_gym_hours_by_day_time(time, day_of_week):
  return GymHour.query.filter(GymHour.start_time < time,
                              GymHour.close_time > time,
                              GymHours.day_of_week == day_of_week).all()

def create_gym_hour(gym_id, day_of_week, open_time, close_time):
  optional_gym_hour = get_gym_hour_by_day_of_week(gym_id, day_of_week)

  if optional_gym_hour is not None:
    return False, optional_gym_hour

  gym = gyms_dao.get_gym_by_id(gym_id)

  if gym is None:
    raise Exception('Gym does not exist.')

  if day_of_week < 0 or day_of_week > 6:
    raise Exception('Invalid day_of_week')

  if open_time > close_time:
    raise Exception('close_time precedes open_time')

  gym_hour = GymHour(
      gym_id = gym_id,
      day_of_week = day_of_week,
      open_time = open_time,
      close_time = close_time
  )
  db_utils.commit_model(gym_hour)
  return True, gym_hour
