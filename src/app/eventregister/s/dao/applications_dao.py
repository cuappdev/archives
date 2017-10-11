from . import *

def create_app(app_name, user_id):
  optional_app = get_app_by_name(app_name)

  if optional_app is not None:
    return False, optional_app

  user = users_dao.get_user_by_id(user_id)

  if user is None:
    raise Exception('User does not exist.')

  app = Application(name=app_name)
  user.applications.append(app)
  db_utils.commit_model(app)

def get_app_by_id(app_id):
  return Application.query.filter(Application.id == app_id).first()

def get_app_by_name(app_name):
  return Application.query.filter(Application.name == app_name).first()

def get_secret_key(app_id):
  optional_app = get_app_by_id(app_id)
  if optional_app is None:
    raise Exception('App does not exist.')
  return optional_app.secret_key

def get_event_types(app_id):
  optional_app = get_app_by_id(app_id)
  if optional_app is None:
    raise Exception('App does not exist.')
  return [event_type.id for event_type in optional_app.event_types]

def is_owned_by_user(app_id, user_id):
  optional_app = get_app_by_id(app_id)
  if optional_app is None:
    raise Exception('App does not exist.')
  return any([user.id == user_id for user in optional_app.users])
