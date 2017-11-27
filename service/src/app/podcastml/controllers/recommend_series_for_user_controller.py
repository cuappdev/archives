from . import *

class RecommendSeriesForUserController(AppDevController):

  def get_path(self):
    return '/series/user/<user_id>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    topic_name = request.view_args['user_id']
    # TODO: retrieve recommended series for this user
    return {'message': 'recommend series for user'}
