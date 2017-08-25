from . import *

class DeleteLikeController(AppDevController):

  def get_path(self):
    return '/likes/<post_id>/'

  def get_methods(self):
    return ['DELETE']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    post_id = request.view_args['post_id']

    likes_dao.delete_like(post_id, user.id)
    return dict()
