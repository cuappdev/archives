from . import *

class GetUserByIdController(AppDevController):

  def get_path(self):
    return '/users/<id>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user_id = request.view_args['id']
    user = users_dao.get_user_by_id(user_id)
    return { 'user': user_schema.dump(user).data }
