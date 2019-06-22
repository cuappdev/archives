from . import *

def get_user_by_id(user_id):
  return User.query.filter(User.id == user_id).first()

def get_user_by_email(email):
  return User.query.filter(User.email == email).first()

def get_user_by_session_token(session_token):
  return User.query.filter(User.session_token == session_token).first()

def get_user_by_update_token(update_token):
  return User.query.filter(User.update_token == update_token).first()

def is_registered(email):
  return get_user_by_email(email) is not None

def verify_credentials(email, password):
  optional_user = get_user_by_email(email)

  if optional_user is None:
    return False, None

  return optional_user.verify_password(password), optional_user

def create_user(email, password, first_name='', last_name=''):
  optional_user = get_user_by_email(email)

  if optional_user is not None:
    return False, optional_user

  # user does not exist
  user = User(
      email=email,
      password=password,
      first_name=first_name,
      last_name=last_name
  )
  db_utils.commit_model(user)
  return True, user

def get_user_apps(user_id):
  optional_user = get_user_by_id(user_id)
  if optional_user is None:
    raise Exception('User does not exist.')
  return optional_user.applications

def clear_all_apps():
  users = User.query.all()
  for user in users:
    user.applications = []
  db_utils.db_session_commit()

def renew_session(update_token):
  user = get_user_by_update_token(update_token)

  if user is None:
    raise Exception('Invalid update token.')

  user.renew_session()
  db_utils.db_session_commit()
  return user
