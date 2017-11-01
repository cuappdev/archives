from functools import wraps
from flask import request
from app.events.dao import users_dao, applications_dao

def authorize_user(f):
  @wraps
  def inner(*args, **kwargs):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
      raise Exception('Missing authorization header.')

    session_token = auth_header.replace('Bearer ', '').strip()
    if session_token is None or not session_token:
      raise Exception('Invalid authorization header.')

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
      raise Exception('Invalid session token.')

    return f(user=user, *args, **kwargs)

  return inner

def authorize_app(f):
  @wraps
  def inner(*args, **kwargs):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
      raise Exception('Missing authorization header.')

    secret_key = auth_header.replace('Bearer ', '').strip()
    if secret_key is None or not secret_key:
      raise Exception('Invalid authorization header.')

    app = applications_dao.get_app_by_secret_key(secret_key)
    if app is None or app.secret_key != secret_key:
      raise Exception('Invalid secret key.')

    return f(app=app, *args, **kwargs)

  return inner
