from . import *

def is_liked_by_user(post_id, user_id):
  optional_like = Like.query.\
    filter(Like.user_id == user_id and Like.post_id == post_id).\
    first()

  return optional_like is not None
