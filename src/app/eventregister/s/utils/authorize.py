from functools import wraps
from flask import session
from app.events.dao import users_dao, applications_dao

def authorize_user(f):
  @wraps
  def inner(*args, **kwargs):
    user_id = session['user_id']

    if user_id is None:
      raise Exception('Invalid user id.')

    user = users_dao.get_user_by_id(user_id)
    return f(user=user, *args, **kwargs)

  return inner

def authorize_app(f):
  @wraps
  def inner(*args, **kwargs):
    secret_key = session['secret_key']

    if secret_key is None:
      raise Exception('Invalid secret key.')

    app = applications_dao.get_app_by_secret_key(secret_key)
    return f(app=app, *args, **kwargs)

  return inner
