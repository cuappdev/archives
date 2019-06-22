from . import *

def is_liked_by_user(post_id, user_id):
  optional_like = Like.query.\
    filter(Like.user_id == user_id and Like.post_id == post_id).\
    first()

  return optional_like is not None

def create_like(post_id, user):
  like = Like(post_id=post_id, user_id=user.id)
  db.session.add(like)
  user.like_count += 1
  try:
    db.session.commit()
    return like
  except Exception:
    db.session.rollback()
    raise Exception('Could not create like')

def delete_like(post_id, user):
  try:
    Post.query.\
      filter(Like.user_id == user.id and Like.post_id == post_id).\
      delete()
    user.like_count -= 1
    db.session.commit()
  except Exception:
    db.session.rollback()
    raise Exception('Could not delete like')
