from . import *

class DeleteFollowingController(AppDevController):

  def get_path(self):
    return '/followings/<followed_id>/'

  def get_methods(self):
    return ['DELETE']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    followed_id = request.view_args['followed_id']
    followings_dao.delete_following(user.id, followed_id)
    return dict()
