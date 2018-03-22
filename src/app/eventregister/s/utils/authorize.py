from functools import wraps
from flask import request
from app.events.dao import users_dao, applications_dao

def auth_bearer(f):
  @wraps(f)
  def inner(*args, **kwargs):
    auth_header = request.headers.get('Authorization')
    print 'auth bearer'
    print auth_header
    if auth_header is None:
      raise Exception('Missing authorization header.')

    bearer_token = auth_header.replace('Bearer ', '').strip()
    if bearer_token is None or not bearer_token:
      raise Exception('Invalid authorization header.')

    return f(bearer_token=bearer_token, *args, **kwargs)

  return inner

def authorize_user(f):
  @wraps(f)
  @auth_bearer
  def inner(*args, **kwargs):
    session_token = kwargs.get('bearer_token')
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
      raise Exception('Invalid session token.')

    return f(user=user, *args, **kwargs)

  return inner

def authorize_app(f):
  @wraps(f)
  @auth_bearer
  def inner(*args, **kwargs):
    print 'auth app'
    secret_key = kwargs.get('bearer_token')
    app = applications_dao.get_app_by_secret_key(secret_key)
    print secret_key, app.serialize()
    if app is None or app.secret_key != secret_key:
      raise Exception('Invalid secret key.')

    return f(app=app, *args, **kwargs)

  return inner
