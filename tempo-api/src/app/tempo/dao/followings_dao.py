from app.tempo.dao.users_dao import *
from . import *

def get_followers(user_id):
  followers = Following.query.filter_by(followed_id=user_id).all()
  return [f.follower for f in followers]

def get_followings(user_id):
  followings = Following.query.filter_by(follower_id=user_id).all()
  return [f.followed for f in followings]

def create_following(follower_id, followed_id):
  try:
    following = Following(follower_id=follower_id, followed_id=followed_id)
    db.session.add(following)
    follower = get_user_by_id(follower_id)
    followed = get_user_by_id(followed_id)
    follower.followings_count += 1
    followed.followers_count += 1
    db.session.commit()
    return follow
  except Exception:
    db.session.rollback()
    raise Exception('Could not create following')

def delete_following(follower_id, followed_id):
  try:
    Following.query.\
      filter(
          Following.follower_id == follower_id \
          and Following.followed_id == followed_id).\
      delete()
    follower = get_user_by_id(follower_id)
    followed = get_user_by_id(followed_id)
    follower.followings_count -= 1
    followed.followers_count -= 1
  except Exception:
    db.session.rollback()
    raise Exception('Could not delete following')
