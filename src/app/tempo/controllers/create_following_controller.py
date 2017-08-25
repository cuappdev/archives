from . import *

class CreateFollowingController(AppDevController):

  def get_path(self):
    return '/followings/'

  def get_methods(self):
    return ['POST']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    followed_id = request.args['followed_id']
    followings_dao.create_following(user.id, follower_id)
    return dict()
