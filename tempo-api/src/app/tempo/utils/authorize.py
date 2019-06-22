from functools import wraps
from flask import request, jsonify
from app.tempo.dao.users_dao import *

def authorize(f):
  @wraps(f)
  def authorization_decorator(*args, **kwargs):
    session_code = request.args['session_code']
    if session_code is None:
      raise Exception('Session code not found!')

    user = get_user_by_valid_session(session_code)
    if user is None:
      raise Exception('Session invalid!')

    return f(user = user, *args, **kwargs)
  return authorization_decorator
