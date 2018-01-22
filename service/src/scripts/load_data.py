import datetime
import json
import os
import sys
from script_utils import * # pylint: disable=W0403

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
set_app_settings()

from app.podcastml.models._all import *
from app.podcastml.utils.db_utils import *

def load_up_db(num_entries=20, length_values=10):
  ids = range(1, num_entries+1)
  lists = [range(uid*length_values, (uid+1)*length_values) for uid in ids]
  strings = [','.join(map(str, lst)) for lst in lists]
  entries = [SeriesForTopic(topic_id=tid, series_list=lst)
             for tid, lst in zip(ids, strings)]
  entries.extend([SeriesForUser(user_id=uid, series_list=lst)
                  for uid, lst in zip(ids, strings)])
  entries.extend([EpisodesForTopic(topic_id=tid, episodes_list=lst)
                  for tid, lst in zip(ids, strings)])
  entries.extend([EpisodesForUser(user_id=uid, episodes_list=lst)
                  for uid, lst in zip(ids, strings)])
  commit_models(entries)
  print('Successfully saved dummy data for ' +
        'SeriesForTopic, SeriesForUser, EpisodesForTopic, EpisodesForUser')

if __name__ == '__main__':
  # Clear these tables
  SeriesForTopic.query.delete()
  EpisodesForTopic.query.delete()
  SeriesForUser.query.delete()
  EpisodesForUser.query.delete()
  db_session_commit()

  # Perform DB transactions
  load_up_db()
