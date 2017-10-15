import os
import sys

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src'
sys.path.append(src_path)

from app import app # pylint: disable=C0413
from app import constants # pylint: disable=C0413
from app.events.models._all import * # pylint: disable=C0413
from app.events.utils.db_utils import * # pylint: disable=C0413

def load_users():
  default_users = [
      User(
          email=constants.TEST_USER_EMAIL,
          password=TEST_USER_PASSWORD,
          first_name='default_first_name1',
          last_name='default_last_name1',
      ),
  ]

  User.query.delete()
  db_session_commit()
  commit_models(default_users)
