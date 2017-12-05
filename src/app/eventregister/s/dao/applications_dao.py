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
  db_utils.commit_model(user)
  return True, app

def get_app_by_id(app_id):
  return Application.query.filter(Application.id == app_id).first()

def get_app_by_name(app_name):
  return Application.query.filter(Application.name == app_name).first()

def get_app_by_secret_key(secret_key):
  return Application.query.filter(Application.secret_key == secret_key).first()

def get_secret_key(app_id):
  optional_app = get_app_by_id(app_id)
  if optional_app is None:
    raise Exception('App does not exist.')
  return optional_app.secret_key

def get_event_types(app_id):
  optional_app = get_app_by_id(app_id)
  if optional_app is None:
    raise Exception('App does not exist.')
  return optional_app.event_types

def get_events(app_id, params={}):
  events = []

  if "event_type" in params:
    event_type = get_event_type_by_name(app_id, name)
    if event_type is None:
      raise Exception('EventType does not exist.')
    else:
      q = Event.query.filter(event_type.id == event_type_id)
  else:
    for event_type in get_event_types(app_id):
      q = Event.query.filter(event_type.id == event_type_id)
  
  if "order_by" in params:
    q = Event.query.order_by(params["order_by"])
  events += q.all()

  return events

def is_owned_by_user(app_id, user_id):
  optional_app = get_app_by_id(app_id)
  if optional_app is None:
    raise Exception('App does not exist.')
  return any([user.id == user_id for user in optional_app.users])
