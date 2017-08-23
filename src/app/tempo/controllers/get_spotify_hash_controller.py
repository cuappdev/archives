from . import *

class GetSpotifyHashController(AppDevController):

  def get_path(self):
    return '/spotify/get_hash/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):

    def _make_authorization_headers(client_id, client_secret):
      auth_header = \
        base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
      return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

    # Fields for POST request
    grant_type = 'authorization_code'
    code = request.args['code']
    redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']

    # Setup requests
    uri = 'https://accounts.spotify.com/api/token'

    # HTTP JSON body
    payload = {
      'grant_type': grant_type,
      'code': code,
      'redirect_uri': redirect_uri
    }

    # HTTP Headers
    headers = _make_authorization_headers(
      os.environ['SPOTIFY_CLIENT_ID'],
      os.environ['SPOTIFY_SECRET']
    )

    r = requests.post(uri, data = payload, headers = headers)
    result = r.json()

    return result
