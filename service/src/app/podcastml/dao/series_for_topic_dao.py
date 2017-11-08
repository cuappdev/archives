from app.podcastml.itunes_top_series_fetcher import *
from . import *

def format_series_list(series_list):
  return ','.join(map(str, series_list))

def generate_series_for_topics():
  topics_to_series = dict(fetch_top_series_all_genres())
  nonexisting_topics = set(topics_to_series.keys())
  current_entries = SeriesForTopic.query.all()
  for entry in current_entries:
    if entry.topic_id in topics_to_series:
      entry.series_list = format_series_list(topics_to_series[entry.topic_id])
      nonexisting_topics.remove(entry.topic_id)
  new_entries = \
  [SeriesForTopic(topic_id=tid,
                  series_list=format_series_list(topics_to_series[tid]))
   for tid in nonexisting_topics]
  db_utils.commit_models(current_entries + new_entries)
