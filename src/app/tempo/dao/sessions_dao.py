from . import *

def create_session_from_user_id(user_id):
  session = Session(user_id=user_id)
  db.session.add(session)
  try:
    db.session.commit()
    return session
  except Exception:
    db.session.rollback()
    raise Exception('Failure creating session from user_id')

def get_or_create_session(user_id):
  optional_session = Session.query.filter_by(user_id=user_id).first()
  return (
      optional_session
      if optional_session is not None
      else create_session_from_user_id(user_id)
  )

def activate_session(session):
  session.is_active = True
  try:
    db.session.commit()
    return session
  except Exception:
    db.session.rollback()
    raise Exception('Could activate session')
