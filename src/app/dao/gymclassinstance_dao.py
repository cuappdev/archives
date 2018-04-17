from datetime import datetime, timedelta

import app.dao.instructors_dao as _id
import app.dao.gyms_dao as gd
import app.dao.gymclass_dao as gcd
import app.dao.class_descs_dao as cd

from . import *

def get_all_gym_class_instances(page, page_size=10):
  if page is None:
    return GymClassInstance.query.limit(page_size).all()
  return GymClassInstance.query.offset(page*page_size).limit(page_size).all()

def get_gym_class_instance_by_id(gym_class_instance_id):
  return GymClassInstance.query.filter(
      GymClassInstance.id == gym_class_instance_id
  ).first()

def get_gym_class_instances_by_gym_class(gym_class_id, page, page_size=10):
  return GymClassInstance.query.filter(
      GymClassInstance.gym_class_id == gym_class_id
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

def delete_gym_classes_by_days_old(days_old):
  GymClassInstance.query.filter(
      GymClassInstance.start_dt < datetime.datetime.today() -
      timedelta(days=days_old)
  ).delete()
  db.session.commit()

def get_gym_class_instances_by_date(date):
  """Takes a string formatted date as input: MM/DD/YYYY
  Example: 03/18/2018 is March 18th, 2018
  """
  input_date = datetime.strpdate(date, '%m/%d/%Y').date()
  return GymClassInstance.query.filter(
      GymClassInstance.start_dt.date() == input_date
  ).all()

def serialize_gym_class_instance(instance):
  serialized_instance = {"id": instance.id}

  gym_class = gcd.get_gym_class_by_id(
      instance.gym_class_id
  )

  # get instructor
  instructor = _id.get_instructor_by_id(
      gym_class.instructor_id
  )
  instructor = instructor_schema.dump(instructor).data
  serialized_instance["instructor"] = instructor

  # get class_desc
  class_desc = cd.get_class_desc_by_id(
      gym_class.class_desc_id
  )
  class_desc = class_desc_schema.dump(class_desc).data
  serialized_instance["class_desc"] = class_desc

  return serialized_instance


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
  class_desc = cd.get_class_desc_by_name(class_name)

  _, gym_class = gcd.create_gym_class(instructor.id, class_desc.id)

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
      is_cancelled=is_cancelled,
      start_dt=start_datetime,
  )
  db_utils.commit_model(gym_class)
  return True, gym_class
