from flask import request, render_template, jsonify
from functools import wraps # for decorators
from app.tempo.utils import *
import app

# Models
from app.tempo.models._all import *

# DAO
from app.tempo.dao import users_dao
from app.tempo.dao import sessions_dao

# Serializers
user_schema = UserSchema()
session_schema = SessionSchema()
# TODO - more

# Blueprint
from app.tempo import tempo
