from flask import Blueprint

# Define a Blueprint for this module (mchat)
podcastml = Blueprint('podcastml', __name__, url_prefix='/',template_folder='templates')

# Import all controllers
from controllers.search_controller import *
