from . import *

def is_registered(email):
  optional_user = User.query.filter(User.email == user_info['email']).first()
  return optional_user is not None

def verify_credentials(email, password):
  optional_user = User.query.filter(User.email == user_info['email']).first()

  if optional_user is not None:
    return False
  return optional_user.password_digest == \
         optional_user.verify_password(password)

def get_or_create_user(user_info):
  if 'email' not in user_info:
    raise Exception('Correct parameters not supplied.')
  optional_user = User.query.filter(User.email == user_info['email']).first()
  if optional_user is not None:
    return False, optional_user

  # user does not exist
  if 'password' not in user_info:
    raise Exception('Correct parameters not supplied.')
  if 'first_name' not in user_info: # init params if missing
    user_info['first_name'] = ''
  if 'last_name' not in user_info:
    user_info['last_name'] = ''

  user = User(
      email=user_info['email'],
      password=user_info['password'],
      first_name=user_info['first_name'],
      last_name=user_info['last_name']
  )
  db_utils.commit_model(user)
  return True, user

def get_apps(email):
  optional_user = User.query.filter(User.email == email).first()
  if optional_user is None:
    raise Exception("User does not exist.")
  return [app.id for app in optional_user.applications] # return app ids
