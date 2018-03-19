import os
import sys

from app import app
from app import constants
from app.gyms.models._all import *
from app.gyms.utils.db_utils import *
from app.gyms.dao import users_dao as ud

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src'
sys.path.append(src_path)

def load_users():
  default_users = [
      User(
          email=constants.TEST_USER_EMAIL,
          first_name='default_first_name1',
          last_name='default_last_name1',
          image_url='default_image_url1'
      ),
  ]

  User.query.delete()
  db_session_commit()
  commit_models(default_users)
