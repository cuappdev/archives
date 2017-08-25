from flask import request, render_template, jsonify, redirect
from functools import wraps # for decorators
from app.tempo.utils import *

# URL-encoding
try: from urllib import urlencode
except ImportError: from urllib.parse import urlencode

import json
import os
import requests

# App instance
import app

# Models
from app.tempo.models._all import *

# DAO
from app.tempo.dao import users_dao, sessions_dao, posts_dao, followings_dao, \
  spotify_creds_dao, likes_dao, songs_dao

# Serializers
user_schema = UserSchema()
session_schema = SessionSchema()
post_schema = PostSchema()
# TODO more

# Workhorse function for post serialization
# b/c there's a lot to serialize
def serialize_post(post, user_id):
  formatted = post_schema.dump(post).data

  # Grab and pop
  song_posts = formatted['song_posts']
  likes = formatted['likes']
  formatted.pop('song_posts')
  formatted.pop('likes')

  # Information to extract
  song = song_posts[0]['song'] if len(song_posts) > 0 else None
  is_liked = len([l for l in likes if l.user_id == user_id]) > 0

  # Fill in fields
  formatted['song'] = song
  formatted['is_liked'] = is_liked

  # return result
  return formatted

# Blueprint
from app.tempo import tempo
