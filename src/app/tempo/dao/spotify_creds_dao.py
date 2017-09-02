import time
import requests
from . import *

def create_or_update_spotify_creds(user_id, token):
  access_token = token['access_token']
  expires_in = token['expires_in']
  refresh_token = token['refresh_token']
  expires_at = str(int(time.time()) + expires_in)

  spotify_cred = SpotifyCred.query.filter_by(user_id=user_id).first()
  if spotify_cred is None:
    spotify_cred = SpotifyCred(
        user_id=user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at
    )
    db.session.add(spotify_cred)
  else:
    spotify_cred.access_token = access_token
    spotify_cred.refresh_token = refresh_token
    spotify_cred.expires_at = expires_at

  try:
    db.session.commit()
    return spotify_cred
  except Exception as e:
    print e
    db.session.rollback()
    raise Exception('Could not save spotify cred!')

def get_spotify_creds_by_user_id(user_id):
  spotify_cred = SpotifyCred.query.filter_by(user_id=user_id).first()

  if spotify_cred is None:
    return spotify_cred

  expires_at = int(spotify_creds.expires_at)
  current_time = int(time.time())

  if expires_at < current_time:
    uri = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': spotify_creds.refresh_token
    }
    headers = make_authorization_headers(
        os.environ['SPOTIFY_CLIENT_ID'],
        os.environ['SPOTIFY_SECRET']
    )
    r = requests.post(uri, data=payload, headers=headers)
    token = r.json()
    spotify_cred = create_or_update_spotify_creds(spotify_cred.user_id, token)

  return spotify_cred
