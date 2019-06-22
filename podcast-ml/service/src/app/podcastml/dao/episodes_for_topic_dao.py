from . import *

def get_episode_list_for_topic(tid):
  return get_list(EpisodesForTopic, 'topic_id', tid, 'episodes_list')
