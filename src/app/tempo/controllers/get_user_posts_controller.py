from . import *

class GetUserPostsController(AppDevController):

  def get_path(self):
    return '/users/<user_id>/posts/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user_id = request.view_args['user_id']
    posts = posts_dao.get_user_posts(user_id)
    return { 'posts': [post_schema.dump(p).data for p in posts] }
