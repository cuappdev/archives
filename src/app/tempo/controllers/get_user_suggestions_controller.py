from . import *

class GetUserSuggestionsController(AppDevController):

  def get_path(self):
    return '/users/suggestions/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    # TODO - get suggestions
    # Approach
    # - Rank users based on mutual followings
    # - Anti-join with following existence
    return dict()
