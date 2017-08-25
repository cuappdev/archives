from flask import Blueprint
from app import *

# Tempo Blueprint
tempo = Blueprint('tempo', __name__, url_prefix = '')

# Import all models
from models._all import *

# Import all controllers
from controllers.user_authentication_controller import *
from controllers.get_feed_controller import *
from controllers.get_user_suggestions_controller import *
from controllers.update_user_username_controller import *
from controllers.get_user_followers_controller import *
from controllers.get_user_followings_controller import *
from controllers.get_spotify_sign_in_uri_controller import *
from controllers.get_spotify_hash_controller import *
from controllers.search_users_controller import *
from controllers.get_is_post_liked_controller import *
from controllers.search_spotify_tracks_controller import *
from controllers.delete_post_controller import *
from controllers.get_user_by_id_controller import *
from controllers.get_user_liked_posts_controller import *
from controllers.create_post_controller import *
from controllers.get_user_posts_controller import *

controllers = [
  UserAuthenticationController(),
  GetFeedController(),
  GetUserSuggestionsController(),
  UpdateUserUsernameController(),
  GetUserFollowersController(),
  GetUserFollowingsController(),
  GetSpotifySignInUriController(),
  GetSpotifyHashController(),
  SearchUsersController(),
  GetIsPostLikedController(),
  SearchSpotifyTracksController(),
  DeletePostController(),
  GetUserByIdController(),
  GetUserLikedPostsController(),
  CreatePostController(),
  GetUserPostsController(),
]

# Setup all controllers
for controller in controllers:
  tempo.add_url_rule(
    controller.get_path(),
    controller.get_name(),
    controller.response,
    methods = controller.get_methods()
  )
