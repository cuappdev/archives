from . import *

def create_user_from_fbid(fbid):
  user = User(fbid = fbid)
  db.session.add(user)
  try:
    db.session.commit()
    return user
  except Exception as e:
    db.session.rollback()
    raise Exception('Failure creating user from fbid')

def get_user_by_fbid(fbid):
  return User.query.filter_by(fbid = fbid).first()

def get_user_from_valid_session(session_code):
  session = Session.query.filter_by(code = session_code).filter_by(is_active = True).first()
  return None if session is None else session.user
