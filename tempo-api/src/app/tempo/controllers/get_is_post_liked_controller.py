from . import *

class GetIsPostLikedController(AppDevController):

  def get_path(self):
    return '/likes/is_liked/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    post_id = request.args['post_id']

    is_liked = likes_dao.is_liked_by_user(post_id, user.id)

    return {'is_liked': is_liked}
