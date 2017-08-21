from . import *
import requests

class UserAuthenticationController(AppDevController):

  def get_path(self):
    return '/users/authenticate/'

  def get_methods(self):
    return ['POST']

  def content(self):
    # Grab user info from Facebook, given access_token
    user_token = request.json['user']['usertoken']
    uri = 'https://graph.facebook.com/me?fields=id&access_token={}'.format(user_token)
    user_info = requests.get(uri).json()
    fbid = user_info['id']

    if fbid is None:
      raise Exception('FBID cannot be null')

    # Grab or create user from FBID
    optional_user = users_dao.get_user_by_fbid(fbid)
    user = (optional_user
      if optional_user is not None
      else users_dao.create_user_from_fbid(fbid))

    result = user_schema.dump(user).data
    print result

    return user_info
