from . import *

def get_or_create_song(song_info):
  optional_song = Song.\
    query.\
    filter_by(spotify_url=song_info['spotify_url']).\
    first()

  if optional_song is not None:
    return optional_song

  song = Song(
      artist=song_info['artist'],
      spotify_url=song_info['spotify_url'],
      track=song_info['track']
  )

  db.session.add(song)
  try:
    db.session.commit()
    return song
  except Exception as e:
    db.session.rollback()
    raise Exception('Could not create song')
