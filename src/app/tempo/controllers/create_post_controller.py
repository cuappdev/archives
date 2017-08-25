from . import *

class CreatePostController(AppDevController):

  def get_path(self):
    return '/posts/'

  def get_methods(self):
    return ['POST']

  @authorize
  def content(self, **kwargs):
    user = kwargs.get('user')
    song_info = request.args['song']

    song = songs_dao.get_or_create_song(song_info)
    post = posts_dao.create_song_post(user.id, song)

    return { 'post': post_schema.dump(post).data }
