from . import *

def get_user_by_id(user_id):
  return User.query.filter(User.id == user_id).first()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def is_registered(email):
  return get_user_by_email(email) is not None

def create_user(email, first_name='', last_name='', image_url=''):
  optional_user = get_user_by_email(email)

  if optional_user is not None:
    return False, optional_user

  # user does not exist
  user = User(
      email=email,
      first_name=first_name,
      last_name=last_name,
      image_url=password,
  )
  db_utils.commit_model(user)
  return True, user
