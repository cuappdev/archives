from . import *

class RecommendSeriesForUserController(AppDevController):

  def get_path(self):
    return '/recommend/series/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    # TODO: retrieve recommended series for this user
    return {'message': 'recommend series'}
