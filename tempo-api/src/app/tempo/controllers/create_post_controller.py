from . import *

class CreatePostController(AppDevController):

  def get_path(self):
    return '/posts/'

  def get_methods(self):
    return ['POST']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    song_info = {
        'spotify_url': request.args['song_info[spotify_url]'],
        'artist': request.args['song_info[artist]'],
        'track': request.args['song_info[track]']
    }
    song = songs_dao.get_or_create_song(song_info)
    post = posts_dao.create_song_post(user.id, song)

    return {'post': serialize_post(post, user.id)}
