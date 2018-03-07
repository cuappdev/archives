from . import *
import datetime

def get_gym_hour(params):
  """Parameterized getter for gym_hours

  params arguments:
  "id" -- the id of gym_hour
  "gym_id" -- the id of the gym of gym_hour
  "day_of_week" -- int from 0 to 6
  "time" -- datetime.time object

  If params contain "id": gets gym_hour with id
  If params contain "gym_id": gets all gym_hours associated with gym_id
  If params contain "gym_id" and "day_of_week": gets gym_hour for gym_id on the
    specficied day_of_week
  If params contain "time" and "day_of_week": gets all gym_hours on day_of_week
    for which time is between open_time and close_time
  """
  keys = params.keys()
  if "id" in keys:
    return GymHour.query.filter(GymHour.id == params["id"]).first()
  if "gym_id" in keys:
    if "day_of_week" in keys:
      return GymHour.query.filter(GymHour.gym_id == params["gym_id"],
                                  GymHour.day_of_week == params["day_of_week"]
                                  ).first()
    else:
      return GymHour.query.filter(GymHour.gym_id == params["gym_id"]).all()
  elif "time" in keys and "day_of_week" in keys:
    return GymHour.query.filter(GymHour.start_time < params["time"],
                                GymHour.close_time > params["time"],
                                GymHour.day_of_week == params["day_of_week"]
                                ).all()
  else:
    raise Exception('No valid parameters')

def create_gym_hour(gym_id, day_of_week, open_time, close_time):
  optional_gym_hour = get_gym_hour({"gym_id": gym_id, "day_of_week": day_of_week})

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
