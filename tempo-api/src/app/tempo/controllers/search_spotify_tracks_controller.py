from . import *

class SearchSpotifyTracksController(AppDevController):

  def get_path(self):
    return '/spotify/search/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    # Info for client request to spotify
    uri = 'https://accounts.spotify.com/api/token'
    payload = {'grant_type': 'client_credentials'}
    headers = make_authorization_headers(
        os.environ['SPOTIFY_CLIENT_ID'],
        os.environ['SPOTIFY_SECRET']
    )

    # Grab AccessToken
    r = requests.post(uri, data=payload, headers=headers)
    access_token = r.json()['access_token']

    # Get data for search request
    base_search_uri = 'https://api.spotify.com/v1/search'
    query = request.args['q']
    params = urlencode({'q': query, 'type': 'track'})
    auth_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    search_uri = '{}?{}'.format(base_search_uri, params)

    # Search
    results = requests.\
        get(search_uri, headers=auth_headers).\
        json()['tracks']['items']

    return {'items': results}
