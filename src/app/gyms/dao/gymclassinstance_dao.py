from datetime import datetime
from . import *

import instructors_dao as _id
import gyms_dao as gd
import gymclass_dao as gcd

def get_all_gym_class_instances(page, page_size=10):
  if page is None:
    return GymClassInstance.query.all()
  return GymClassInstance.query.paginate(int(page), page_size, False)

def get_gym_class_instance_by_id(gym_class_instance_id):
  return GymClassInstance.query.filter(
      GymClassInstance.id == gym_class_instance_id
  ).first()

def get_gym_class_instances_by_gym_class(gym_class_name, page, page_size=10):
  return GymClassInstance.query.filter(
      GymClassInstance.gym_class == gym_class_name
  ).paginate(page, page_size, False)

def get_gym_class_by_start_duration(gym_class_id, gym_id, start_dt, duration):
  return GymClassInstance.query.filter(
      GymClassInstance.gym_id == gym_id,
      GymClassInstance.gym_class_id == gym_class_id,
      GymClassInstance.start_dt == start_dt,
      GymClassInstance.duration == duration
  )

def get_all_classes_by_start_duration(start_dt, duration):
  return GymClassInstance.query.filter(
      GymClassInstance.start_dt == start_dt,
      GymClassInstance.duration == duration
  )

def get_gym_class_instances_not_cancelled():
  return GymClassInstance.query.filter(
      GymClassInstance.is_cancelled == False
  ).all()

def get_gym_class_instances_by_time(time):
  """Gets all class instances that occur in
   time and returns a list of all class instances"""
  return GymClassInstance.query.filter(
      GymClassInstance.start_dt < time,
      GymClassInstance.start_dt + GymClassInstance.duration > time
  ).all()

def get_gym_class_instance_by_instructor(instructor_id):
  return GymClassInstance.query.filter(
      GymClassInstance.instructor_id == instructor_id
  ).all()

def create_gym_class_instance(args):
  class_name = args.get("class_name")
  date = args.get("date")
  gym_name = args.get("location")
  instructor_name = args.get("instructor_name")
  is_cancelled = args.get("is_cancelled")
  start_time = args.get("start_time")
  end_time = args.get("end_time")

  _, instructor = _id.create_instructor(instructor_name)
  _, gym = gd.create_gym(gym_name)
  gym_class = gcd.get_gym_class_by_name(class_name)

  if start_time is None or end_time is None:
    start_datetime = None
    duration = None
  else:
    start_datetime = datetime.datetime.strptime(start_time, '%I:%M%p')
    end_datetime = datetime.datetime.strptime(end_time, '%I:%M%p')
    if end_datetime > start_datetime: # scraped data is inconsistent
      duration = end_datetime - start_datetime
    else:
      duration = start_dateime - end_datetime

    start_datetime = datetime.datetime.strptime( # add date
        date + " " + start_time, '%m/%d/%Y %I:%M%p'
    )


  optional_instance = GymClassInstance.query.filter(
      GymClassInstance.gym_id == gym.id,
      GymClassInstance.gym_class_id == gym_class.id,
      GymClassInstance.instructor_id == instructor.id,
      GymClassInstance.start_dt == start_datetime,
      GymClassInstance.duration == duration,
  ).first()

  if optional_instance is not None:
    if is_cancelled != optional_instance.is_cancelled:
      optional_instance.is_cancelled = is_cancelled
      db_utils.commit_model(optional_instance)
    return False, optional_instance

  gym_class = GymClassInstance(
      duration=duration,
      gym_id=gym.id,
      gym_class_id=gym_class.id,
      name=class_name,
      instructor_id=instructor.id,
      is_cancelled=is_cancelled,
      start_dt=start_datetime,
  )
  db_utils.commit_model(gym_class)
  return True, gym_class
