from . import *

def get_gym_class_instance_by_id(gym_class_instance_id):
  return GymClassInstance.query.filter(
      GymClassInstance.id == gym_class_instance_id
  ).first()

def get_gym_class_instances_by_gym_class(gym_class_name, page, page_size=10):
  return GymClassInstance.query.filter(
      GymClassInstance.gym_class == gym_class_name
  ).paginate(page, page_size, False)

def get_gym_class_by_start_duration(gym_class_id, gym_id, start_time, duration):
  return GymClassInstance.query.filter(
      GymClassInstance.gym_id == gym_id,
      GymClassInstance.gym_class_id == gym_class_id,
      GymClassInstance.start_time == start_time,
      GymClassInstance.duration == duration
  )

def get_all_classes_by_start_duration(start_time, duration):
  return GymClassInstance.query.filter(
      GymClassInstance.start_time == start_time,
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
      GymClassInstance.start_time < time,
      GymClassInstance.start_time + GymClassInstance.duration > time
  ).all()

def create_gym_class_instance(gym_class_id, gym_id, instructor_id, start_time, duration):
  optional_gym_class_instance = GymClassInstance.query.filter(
      GymClassInstance.gym_class_id = gym_class_id,
      GymClassInstance.gym_id = gym_id,
      GymClassInstance.instructor_id = instructor_id,
      GymClassInstance.start_time = start_time,
      GymClassInstance.duration = duration
  ).first()

  if optional_gym_class_instance is not None:
    return False, optional_gym_class_instance

  gym_class = gymclass_dao.get_gym_class_by_id(gym_class_id)

  if gym_class is None:
    raise Exception('Gym class does not exist.')

  gym_class_instance = GymClassInstance(
      gym_class_id=gym_class_id,
      gym_id=gym_id,
      instructor_id=instructor_id,
      start_time=start_time,
      duration=duration
  )
  db_utils.commit_model(gym_class_instance)
  return True, gym_class_instance
