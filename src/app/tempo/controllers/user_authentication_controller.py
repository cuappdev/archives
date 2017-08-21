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

    # TODO - find user by FBID
    # TODO - create / find session
    # TODO - respond
    print fbid
    return user_info
