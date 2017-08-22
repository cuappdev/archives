from . import *

class UpdateUserUsernameController(AppDevController):

  def get_path(self):
    return '/users/update_username/'

  def get_methods(self):
    return ['POST']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    username = request.args['username']
    updated_user = users_dao.update_user_username(user, username)
    return { 'user': user_schema.dump(updated_user).data }
