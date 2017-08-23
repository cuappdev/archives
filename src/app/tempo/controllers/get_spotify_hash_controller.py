from . import *
from flask import redirect
import base64
import json
import os
import requests

class GetSpotifyHashController(AppDevController):

  def get_path(self):
    return '/spotify/get_hash/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    # Fields for POST request
    grant_type = 'authorization_code'
    code = request.args['code']
    redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']

    # Setup requests
    uri = 'https://accounts.spotify.com/api/token'
    authorization = base64.b64encode(bytes(
      'Basic {0}:{1}'.\
        format(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_SECRET']),
      'utf-8'
    ))

    # HTTP JSON body
    payload = {
      'grant_type': grant_type,
      'code': code,
      'redirect_uri': redirect_uri
    }

    # Request result
    r = requests.post(url, data = json.dumps(payload))
    r['Authorization'] = authorization
    result = r.json()
    print result
    return result
