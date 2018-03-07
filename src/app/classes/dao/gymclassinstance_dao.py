from . import *
import datetime

def get_gym_class_instance_by_id(gym_class_instance_id):
  return GymClassInstance.query.filter(GymClassInstance.id == gym_class_instance_id).first()

def get_gym_class_instances_by_gym_class(gym_class_name):
  return GymClassInstance.query.filter(GymClassInstance.gym_class == gym_class_name).all()

def get_gym_class_instances_not_cancelled():
  return GymClassInstance.query.filter(GymClassInstance.is_cancelled == False).all()

def get_gym_class_instances_by_time(time):
  return GymClassInstance.query.filter(GymClassInstance.start_time < time,
                                       GymClassInstance.start_time + GymClassInstance.duration > time).all()

def get_gym_class_instances_by_class_time(gym_class_name, time):
  return GymClassInstance.query.filter(GymClassInstance.gym_class = gym_class_name,
                                       GymClassInstance.start_time < time,
                                       GymClassInstance.start_time + GymClassInstance.duration > time).all()

def create_gym_class_instance(gym_class_id, start_time, duration):
  gym_class = gymclass_dao.get_gym_class_by_id(gym_class_id)

  if gym_class is None:
    raise Exception('Gym class does not exist.')

  gym_class_instance = GymClassInstance(
      gym_class_id=gym_class_id,
      start_time=start_time,
      duration=duration
  )
  db_utils.commit_model(gym_class_instance)
  return True, gym_class_instance
