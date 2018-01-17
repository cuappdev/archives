from . import *

def get_episode_list_for_topic(tid):
  optional_episodes_for_topic = EpisodesForTopic.query \
    .filter(EpisodesForTopic.topic_id == tid).first()
  if optional_episodes_for_topic:
    return extract_list(optional_episodes_for_topic.episodes_list)
  else:
    raise Exception('Topic with id {} does not exist.'.format(tid))
