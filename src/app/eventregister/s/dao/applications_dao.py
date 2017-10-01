from . import *

def create_app(app_name, email):
  app = Application(name=app_name)
  user = users_dao.get_or_create_user({'email': email})
  user.applications.append(app)
  db_utils.commit_model(app)

def get_secret_key(app_name):
  optional_app = Application.query.filter(Application.name == app_name).first()
  if optional_app is None:
    raise Exception("App does not exist.")
  return optional_app.secret_key

def get_event_types(app_name):
  optional_app = Application.query.filter(Application.name == app_name).first()
  if optional_app is None:
    raise Exception("App does not exist.")
  return optional_app.event_types
