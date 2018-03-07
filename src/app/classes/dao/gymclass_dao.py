from . import *

def get_gym_class_by_id(gym_class_id):
  return GymClass.query.filter(GymClass.id == gym_class_id).first()

def get_gym_classes_by_gym(gym_id):
  return GymClass.query.filter(GymClass.gym == gym_id).all()

def get_gym_classs_by_name_loc_instuct(name, gym_id, instructor):
  return GymClass.query.fiter(GymClass.name = name,
                              GymClass.gym_id = gym_id,
                              GymClass.instructor = instructor)

def get_gym_classes_by_instructor(instructor_id):
  return GymClass.query.filter(GymClass.instructor_id == instructor_id).all()

def create_gym_class(name, gym_id, description='', instructor=''):
  optional_gym_class = get_gym_class_by_name_loc_instruct()

  if optional_gym_class is not None:
     return False, optional_gym_class

  gym = gyms_dao.get_gym_by_id(gym_id)

  if gym is None:
    raise Exception('Gym does not exist.')

  gym_class = GymClass(
      gym_id=gym_id,
      name=name,
      description=description,
      instructor=instructor
  )
  db_utils.commit_model(gym_class)
  return True, gym_class
