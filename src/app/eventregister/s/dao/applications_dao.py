from sqlalchemy import in_
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

def get_events(app_id, params):
  if "event_type_ids" in params:
    q = Event.query.filter(
        event_type.id.in_(params["event_type_ids"])
        )
  else:
    q = Event.query.filter(event_type.application_id == app_id)

  if "order_by" in params:
    if params["order_by"] == "timestamp":
      if params.get("order_by_direction") == "asc":
        q = q.order_by(Event.created_at) # asc is default
      else: # desc or not passed
        q = q.order_by(Event.created_at.desc())
    else:
      raise Exception("Invalid value for 'order_by'")
  else:
    q = q.order_by(Event.created_at.desc())

  if "offset" in params:
    q = q.offset(params["offset"])

  if "max" in params:
    q = q.limit(params["max"])
  else:
    q = q.limit(20)

  return q.all()

def is_owned_by_user(app_id, user_id):
  optional_app = get_app_by_id(app_id)
  if optional_app is None:
    raise Exception('App does not exist.')
  return any([user.id == user_id for user in optional_app.users])

def reset_secret_key(app_id):
  optional_app = get_app_by_id(app_id)
  if optional_app is None:
    raise Exception('App does not exist.')

  optional_app.reset_secret_key()
  return optional_app.secret_key
