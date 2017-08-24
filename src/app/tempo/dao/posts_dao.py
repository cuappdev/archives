from . import *
from datetime import datetime, timedelta
from sqlalchemy import desc

def get_feed(user_id):
  one_day_ago = datetime.today() - timedelta(days = 1)

  followers_posts_query = Post.query.\
    join(Following, Following.follower_id == user_id and Post.user_id == Following.followed_id).\
    filter(Post.created_at >= one_day_ago)

  my_posts_query = Post.query.\
    filter(Post.user_id == user_id).\
    filter(Post.created_at >= one_day_ago)

  feed_query = followers_posts_query.\
    union(my_posts_query).\
    order_by(desc(Post.created_at))

  return feed_query.all()

def get_user_posts(user_id):
  return Post.query.filter_by(user_id = user_id).all()

def create_song_post(user_id, song):
  try:
    post = Post(user_id = user_id)
    db.session.add(post)
    db.session.flush() # to get post.id
    song_post = SongPost(post_id = post.id, song_id = song.id)
    db.session.commit()
    return post
  except Exception as e:
    db.session.rollback()
    raise Exception('Could not activate song post')
