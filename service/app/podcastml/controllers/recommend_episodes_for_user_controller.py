from . import *

class RecommendEpisodesForUserController(AppDevController):

  def get_path(self):
    return '/recommend/episodes/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    # TODO: retrieve recommended episodes for this user
    return {'message': 'recommend episodes'}
