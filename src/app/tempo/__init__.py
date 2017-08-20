from flask import Blueprint
from app import *

# Tempo Blueprint
tempo = Blueprint('tempo', __name__, url_prefix = '/tempo')

# Import all models
from models._all import *

# Import all endpoints
# TODO
