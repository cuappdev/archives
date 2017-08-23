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

def get_user_by_valid_session(session_code):
  session = Session.query.filter_by(code = session_code).filter_by(is_active = True).first()
  return None if session is None else session.user

def get_suggested_users(user_id, limit):
  sql = db.text("""
  SELECT Temp.id
  FROM (
    SELECT u.id AS id, COUNT(f1.follower_id) AS mutual_followers
    FROM users u, followings f1, followings f2
    WHERE {0} = f1.followed_id
    AND u.id = f2.followed_id
    AND f1.follower_id = f2.follower_id
    AND NOT EXISTS (
      SELECT followed_id
      FROM followings
      WHERE u.id = followed_id
      AND {0} = follower_id
    )
    GROUP BY u.id, f1.follower_id
  ) as Temp
  ORDER BY Temp.mutual_followers DESC
  LIMIT {1}
  """.format(user_id, limit))

  top_suggested_ids = [row['id'] for row in db.engine.execute(sql)]
  return [] if len(top_suggested_ids) == 0 \
    else User.query.filter(User.id.in_(top_suggested_ids)).all()

def update_user_username(user, username):
  user.username = username
  # db.session.add(user)
  try:
    db.session.commit()
    return user
  except Exception as e:
    db.session.rollback()
    raise Exception('Failure updating user username')

def query_users(query):
  return User.query.filter(User.username.like('%{}%'.format(query))).all()
