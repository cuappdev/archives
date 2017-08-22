from . import *

class GetUserFollowingsController(AppDevController):

  def get_path(self):
    return '/users/<user_id>/followings/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user_id = request.view_args['user_id']
    followings = followings_dao.get_followings(user_id)
    return { 'followings': [user_schema.dump(u).data for u in followings] }
