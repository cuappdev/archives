from . import *

class CreateLikeController(AppDevController):

  def get_path(self):
    return '/likes/'

  def get_methods(self):
    return ['POST']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    post_id = request.args['post_id']

    likes_dao.create_like(post_id, user.id)
    return dict()
