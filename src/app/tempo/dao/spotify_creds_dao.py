from . import *

def get_spotify_creds_by_user_id(user_id):
  return SpotifyCred.query.filter_by(user_id = user_id).first()
