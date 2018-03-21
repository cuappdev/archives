from . import *

def get_all_class_descs():
  return ClassDesc.query.all()

def get_class_desc_by_id(gym_class_id):
  return ClassDesc.query.filter(ClassDesc.id == gym_class_id).first()

def get_class_desc_by_name(name):
  return ClassDesc.query.filter(ClassDesc.name == name).first()

def create_class_desc(name, description=''):
  optional_class_desc = get_class_desc_by_name(name)

  if optional_class_desc is not None:
     return False, optional_class_desc

  new_class = ClassDesc(name=name, description=description)
  db_utils.commit_model(new_class)
  return True, new_class
