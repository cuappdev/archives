from . import *

class GetUserLikedPostsController(AppDevController):

  def get_path(self):
    return '/users/<user_id>/likes'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user_id = request.view_args['user_id']
    posts = posts_dao.get_user_liked_posts(user_id)
    return { 'posts': [serialize_post(p) for p in posts] }
