from . import *

class DeletePostController(AppDevController):

  def get_path(self):
    return '/posts/<post_id>/'

  def get_methods(self):
    return ['DELETE']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    post_id = request.view_args['post_id']

    posts_dao.delete_song_post(user.id, post_id)

    return dict()
