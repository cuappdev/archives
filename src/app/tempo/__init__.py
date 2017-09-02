from flask import Blueprint
from app import *

# Tempo Blueprint
tempo = Blueprint('tempo', __name__, url_prefix='')

# Import all models
from app.tempo.models._all import * # pylint: disable=C0413

# Import all controllers
from app.tempo.controllers.create_following_controller import * # pylint: disable=C0413
from app.tempo.controllers.create_like_controller import * # pylint: disable=C0413
from app.tempo.controllers.create_post_controller import * # pylint: disable=C0413
from app.tempo.controllers.delete_following_controller import * # pylint: disable=C0413
from app.tempo.controllers.delete_like_controller import * # pylint: disable=C0413
from app.tempo.controllers.delete_post_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_feed_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_is_post_liked_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_spotify_hash_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_spotify_sign_in_uri_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_user_by_id_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_user_followers_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_user_followings_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_user_liked_posts_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_user_posts_controller import * # pylint: disable=C0413
from app.tempo.controllers.get_user_suggestions_controller import * # pylint: disable=C0413
from app.tempo.controllers.save_songs_to_spotify_controller import * # pylint: disable=C0413
from app.tempo.controllers.search_spotify_tracks_controller import * # pylint: disable=C0413
from app.tempo.controllers.search_users_controller import * # pylint: disable=C0413
from app.tempo.controllers.update_user_username_controller import * # pylint: disable=C0413
from app.tempo.controllers.user_authentication_controller import * # pylint: disable=C0413

controllers = [
    CreateFollowingController(),
    CreateLikeController(),
    CreatePostController(),
    DeleteFollowingController(),
    DeleteLikeController(),
    DeletePostController(),
    GetFeedController(),
    GetIsPostLikedController(),
    GetSpotifyHashController(),
    GetSpotifySignInUriController(),
    GetUserByIdController(),
    GetUserFollowersController(),
    GetUserFollowingsController(),
    GetUserLikedPostsController(),
    GetUserPostsController(),
    GetUserSuggestionsController(),
    SaveSongsToSpotifyController(),
    SearchSpotifyTracksController(),
    SearchUsersController(),
    UpdateUserUsernameController(),
    UserAuthenticationController(),
]

# Setup all controllers
for controller in controllers:
  tempo.add_url_rule(
      controller.get_path(),
      controller.get_name(),
      controller.response,
      methods=controller.get_methods()
  )
