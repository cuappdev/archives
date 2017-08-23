from . import *

class UserAuthenticationController(AppDevController):

  def get_path(self):
    return '/users/authenticate/'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    user_token = request.json['user']['usertoken']
    uri = 'https://graph.facebook.com/me?fields=id&access_token={}'.format(user_token)
    user_info = requests.get(uri).json()
    fbid = user_info['id']

    if fbid is None:
      raise Exception('FBID cannot be null')

    optional_user = users_dao.get_user_by_fbid(fbid)

    # User
    user = (
      optional_user
      if optional_user is not None
      else users_dao.create_user_from_fbid(fbid)
    )

    # Session
    session_pre_activate = sessions_dao.get_or_create_session(user.id)
    session = sessions_dao.activate_session(session_pre_activate)

    # Newness
    is_new_user = optional_user is None

    return {
      'user': user_schema.dump(user).data,
      'session': session_schema.dump(session).data,
      'new_user': is_new_user
    }
