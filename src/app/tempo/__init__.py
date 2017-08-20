from flask import Blueprint
from app import *

# Tempo Blueprint
tempo = Blueprint('tempo', __name__, url_prefix = '/tempo')

# Import all endpoints
# TODO
