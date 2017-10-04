from . import *

def get_user_by_id(user_id):
  return User.query.filter(User.id == user_id).first()

def get_user_by_email(email):
  return User.query.filter(User.email == email).first()

def is_registered(email):
  return get_user_by_email(email) is not None

def verify_credentials(email, password):
  optional_user = get_user_by_email(email)

  if optional_user is None:
    return False
  
  return optional_user.verify_password(password)

def create_user(email, password, first_name='', last_name=''):
  optional_user = get_user_by_email(email)
  
  if optional_user is not None:
    return False, optional_user

  # user does not exist
  user = User(email=email, password=password,
              first_name=first_name, last_name=last_name)
  db_utils.commit_model(user)
  return True, user

def get_apps(user_id):
  optional_user = get_user_by_id(user_id)
  if optional_user is None:
    raise Exception('User does not exist.')
  return [app.id for app in optional_user.applications] # return app ids
