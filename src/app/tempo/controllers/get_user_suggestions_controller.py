from . import *

class GetUserSuggestionsController(AppDevController):

  def get_path(self):
    return '/users/suggestions/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    suggested_users = users_dao.get_suggested_users(user.id, 20)
    return { 'users': [user_schema.dump(u).data for u in suggested_users] }
