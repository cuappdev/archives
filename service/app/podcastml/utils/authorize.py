import datetime
import os
from functools import wraps
from flask import request, jsonify

def authorize(f):
  @wraps(f)
  def authorization_decorator(*args, **kwargs):
    api_key = request.headers.get('api_key')
    if api_key is None:
      raise Exception('API key is not included!')
    elif api_key != os.environ['API_KEY']:
      raise Exception('Invalid API key!')

    return f(*args, **kwargs)
  return authorization_decorator
