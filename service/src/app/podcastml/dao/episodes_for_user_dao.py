from . import *

def get_episode_list_for_user(uid):
  return get_list(EpisodesForUser, 'user_id', uid, 'episodes_list')
