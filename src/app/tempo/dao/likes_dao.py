from . import *

def is_liked_by_user(post_id, user_id):
  optional_like = Like.query.\
    filter(Like.user_id == user_id and Like.post_id == post_id).\
    first()

  return optional_like is not None

def create_like(post_id, user_id):
  like = Like(post_id = post_id, user_id = user_id)
  db.session.add(like)
  try:
    db.session.commit()
    return like
  except Exception as e:
    db.session.rollback()
    raise Exception('Could not create like')

def delete_like(post_id, user_id):
  try:
    Post.query.\
      filter(Like.user_id == user_id and Like.post_id == post_id).\
      delete()
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    raise Exception('Could not delete like')
