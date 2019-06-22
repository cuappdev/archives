from . import *

class GetSpotifySignInUriController(AppDevController):

  def get_path(self):
    return '/spotify/sign_in_uri/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')

    # Compose URI
    params = urlencode({
        'client_id': os.environ['SPOTIFY_CLIENT_ID'],
        'response_type': 'code',
        'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI'],
        'state': user.session.code
    })
    uri = 'https://accounts.spotify.com/authorize?{}'.format(params)

    return {'uri': uri}
