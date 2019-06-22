from . import *

def get_series_list_for_user(uid):
  return get_list(SeriesForUser, 'user_id', uid, 'series_list')
