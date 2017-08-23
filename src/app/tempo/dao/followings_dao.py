from . import *

def get_followers(user_id):
  followers = Following.query.filter_by(followed_id = user_id).all()
  return [f.follower for f in followers]

def get_followings(user_id):
  followings = Following.query.filter_by(follower_id = user_id).all()
  return [f.followed for f in followings]
