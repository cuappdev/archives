from . import *

class CreateUserController(AppDevController):
  def get_path(self):
    return '/users/'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    email = kwargs.get('email')
    password = kwargs.get('password')
    first_name = kwargs.get('first_name')
    last_name = kwargs.get('last_name')

    # include first/last names as dao argument only if not none
    names = {}

    if first_name is not None:
      names['first_name'] = first_name

    if last_name is not None:
      names['last_name'] = last_name

    created, user = users_dao.create_user(email, password, **names)

    if not created:
      raise Exception('User already exists.')
    
    return {'user': user}
