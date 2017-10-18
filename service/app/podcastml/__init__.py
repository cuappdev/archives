from flask import Blueprint
from app.podcastml.utils import redisConnector

# Define a Blueprint for this module (mchat)
podcastml = Blueprint('podcastml', __name__, url_prefix='/api/v1')
redisConn = redisConnector.RedisConn("podcastML", "host")

# Import all controllers
from app.podcastml.controllers.recommend_episodes_for_user_controller import *
from app.podcastml.controllers.recommend_series_for_user_controller import *

controllers = [
    RecommendSeriesForUserController(),
    RecommendEpisodesForUserController()
]

# Setup all controllers
for controller in controllers:
  podcastml.add_url_rule(
      controller.get_path(),
      controller.get_name(),
      controller.response,
      methods=controller.get_methods()
  )
