from . import *

def get_gym_class_by_id(gym_class_id):
  return GymClass.query.filter(GymClass.id == gym_class_id).first()

def get_gym_class_instance_by_name(name):
  return GymClass.query.filter(GymClass.name == gym_class_id).first()

def create_gym_class(name, description=''):
  optional_gym_class = get_gym_class_by_name(name)

  if optional_gym_class is not None:
     return False, optional_gym_class

  gym = gyms_dao.get_gym_by_id(gym_id)

  if gym is None:
    raise Exception('Gym does not exist.')

  gym_class = GymClass(name=name, description=description)
  db_utils.commit_model(gym_class)
  return True, gym_class
