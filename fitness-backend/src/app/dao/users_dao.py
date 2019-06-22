from . import *

def get_user_by_id(user_id):
  return User.query.filter(User.id == user_id).first()

def get_user_by_device_id(device_id):
  return User.query.filter(User.device_id == device_id).first()

def is_registered(device_id):
  return get_user_by_device_id(device_id) is not None

def get_user_classes(user_id):
  optional_user = get_user_by_id(user_id)
  if optional_user is None:
    raise Exception('User does not exist.')
  return optional_user.gym_classes

def create_user(device_id):
  optional_user = get_user_by_device_id(device_id)

  if optional_user is not None:
    return False, optional_user

  # user does not exist
  user = User(
      device_id=device_id,
  )
  db_utils.commit_model(user)
  return True, user
