from . import *

def get_gym_class_by_id(gym_class_id):
  return GymClass.query.filter(GymClass.id == gym_class_id).first()

def get_gym_classes_by_instructor(instructor_id):
  return GymClass.query.filter(
      GymClass.instructor_id == instructor_id
  ).all()

def get_all_classes():
  return GymClass.query.all()

def create_gym_class(instructor_id, class_desc_id):
  optional_class = GymClass.query.filter(
      GymClass.instructor_id == instructor_id,
      GymClass.class_desc_id == class_desc_id
  ).first()

  if optional_class is not None:
     return False, optional_class

  new_gymclass = \
    GymClass(instructor_id=instructor_id, class_desc_id=class_desc_id)
  db_utils.commit_model(new_gymclass)
  return True, new_gymclass
