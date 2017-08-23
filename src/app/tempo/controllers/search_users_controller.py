from . import *

class SearchUsersController(AppDevController):

  def get_path(self):
    return '/users/search/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    query = request.args['q'].lower()
    users = users_dao.query_users(query)
    return { 'users': [user_schema.dump(u).data for u in users] }
