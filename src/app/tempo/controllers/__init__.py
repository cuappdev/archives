from flask import request, render_template, jsonify, redirect
from functools import wraps # for decorators
from app.tempo.utils import *

# URL-encoding
try: from urllib import urlencode
except ImportError: from urllib.parse import urlencode

import base64
import json
import os
import requests
import six

# App instance
import app

# Models
from app.tempo.models._all import *

# DAO
from app.tempo.dao import users_dao, sessions_dao, posts_dao, followings_dao, \
  spotify_creds_dao

# Serializers
user_schema = UserSchema()
session_schema = SessionSchema()
post_schema = PostSchema()
# TODO more

# Blueprint
from app.tempo import tempo
