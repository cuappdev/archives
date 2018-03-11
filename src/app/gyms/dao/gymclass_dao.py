from . import *

def get_gym_class_by_id(gym_class_id):
  return GymClass.query.filter(GymClass.id == gym_class_id).first()

def get_gym_class_by_name(name):
  return GymClass.query.filter(GymClass.name == name).first()

def create_gym_class(name, description=''):
  optional_gym_class = get_gym_class_by_name(name)

  if optional_gym_class is not None:
     return False, optional_gym_class

  gym_class = GymClass(name=name, description=description)
  db_utils.commit_model(gym_class)
  return True, gym_class
