from . import *

class GetFeedController(AppDevController):

  def get_path(self):
    return '/feed/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    # TODO - grab feed, but we can get user now!
    user = kwargs.get('user')
    print user
    return { 'we': 'got it!' }
