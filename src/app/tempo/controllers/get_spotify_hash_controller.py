from . import *

class GetSpotifyHashController(AppDevRedirectController):

  def get_path(self):
    return '/spotify/get_hash/'

  def get_methods(self):
    return ['GET']

  def make_uri(self, **kwargs):
    # Fields for POST request
    grant_type = 'authorization_code'
    code = request.args['code']
    redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']
    session_code = request.args['state']

    # Setup requests
    uri = 'https://accounts.spotify.com/api/token'

    # HTTP JSON body
    payload = {
      'grant_type': grant_type,
      'code': code,
      'redirect_uri': redirect_uri
    }

    # HTTP Headers
    headers = make_authorization_headers(
      os.environ['SPOTIFY_CLIENT_ID'],
      os.environ['SPOTIFY_SECRET']
    )

    r = requests.post(uri, data = payload, headers = headers)
    token = r.json()

    # Compose redirect uri
    uri = '{0}callback?access_token={1}&session_code={2}&expires_at={3}'.\
      format(
        os.environ['TEMPO_REDIRECT'],
        token['access_token'],
        session_code,
        token['expires_in']
      )

    return uri
