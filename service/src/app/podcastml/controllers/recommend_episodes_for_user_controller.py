from . import *

class RecommendEpisodesForUserController(AppDevController):

  def get_path(self):
    return '/episodes/user/<user_id>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    topic_name = request.view_args['user_id']
    # TODO: retrieve recommended episodes for this user
    return {'message': 'recommend episodes for user'}
