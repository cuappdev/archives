from . import *

class GetUserFollowersController(AppDevController):

  def get_path(self):
    return '/users/<user_id>/followers/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user_id = request.view_args['user_id']
    followers = followings_dao.get_followers(user_id)
    return {'followers': [user_schema.dump(u).data for u in followers]}
