from . import *

def create_user_from_fbid(fbid):
  user = User(fbid = fbid)
  db.session.add(user)
  try:
    db.session.commit()
    return user
  except Exception as e:
    print e
    db.session.rollback()
    raise Exception('Failure creating user from fbid')

def get_user_by_fbid(fbid):
  return User.query.filter_by(fbid = fbid).first()
