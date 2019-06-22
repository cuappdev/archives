from . import *

class SaveSongsToSpotifyController(AppDevController):

  def get_path(self):
    return '/spotify/save_songs'

  def get_methods(self):
    return ['POST']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    ids = request.args['ids']

    # Spotify request to like the song!
    spotify_creds = spotify_creds_dao.get_spotify_creds_by_user_id(user.id)
    headers = {'Authorization': 'Bearer {}'.format(spotify_creds.access_token)}
    uri = 'https://api.spotify.com/v1/me/tracks?ids={}'.format(ids)
    r = requests.put(uri, headers=headers)

    # Respond based on status_code
    if r.status_code != 200:
      raise Exception('Unable to save spotify songs!')
    else:
      return dict()
