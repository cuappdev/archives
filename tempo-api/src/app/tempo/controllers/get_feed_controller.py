from . import *

class GetFeedController(AppDevController):

  def get_path(self):
    return '/feed/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    posts = posts_dao.get_feed(user.id)
    return {'posts':  [serialize_post(p, user.id) for p in posts]}