"""Init function for blueprinting."""
from flask import Blueprint
from podcastml.utils import redisConnector
# Define a Blueprint for this module (mchat)
podcastml = Blueprint(
    'podcastml',
    __name__,
    url_prefix='/',
    template_folder='templates')
redisConn = redisConnector.redisConn("podcastML", "host")

# Import all controllers
