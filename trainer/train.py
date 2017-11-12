# Created for PySpark 2.2.0

import os
from collections import defaultdict

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.linalg.distributed import CoordinateMatrix
from appdev.connectors import MySQLConnector, RedisConnector

entry_redis_key = 'training_entries'

weights = {
    'recommendations': 0.5,
    'bookmarks': 0.1,
    'listening_histories': 0.2,
    'subscriptions': 0.2
}

def get_matrix_entries():
  conn = MySQLConnector(os.environ['DB_USERNAME'],
                        os.environ['DB_PASSWORD'],
                        os.environ['DB_HOST'],
                        os.environ['DB_NAME'])

  # table name -> (user_id index, episode_id index)
  db_tables = {
      'recommendations': (3, 4),
      'bookmarks': (3, 4),
      'listening_histories': (4, 5)
  }

  matrix_entries = defaultdict(float)  # (user_id, episode_id) -> score

  for table, (user_index, episode_index) in db_tables.iteritems():
    rows = conn.read_batch(table)
    for row in rows:
      user_id, episode_id = row[user_index], row[episode_index]
      matrix_entries[(user_id, episode_id)] += weights[table]

  rows = conn.read_batch('subscriptions')
  series_to_users = defaultdict(list)
  for row in rows:
    user_id, series_id = row[3], row[4]
    series_to_users[series_id].append(user_id)

  conn.close()

  conn_podcast = MySQLConnector(os.environ['DB_USERNAME'],
                                os.environ['DB_PASSWORD'],
                                os.environ['DB_HOST'],
                                os.environ['PODCAST_DB_NAME'])

  episode_query = 'SELECT id FROM episodes WHERE series_id={}'

  rows = conn_podcast.execute_batch(
      [episode_query.format(series_id) for series_id in series_to_users])
  for (series_id, episode_list) in zip(series_to_users, rows):
    for row in episode_list:
      episode_id = row[0]
      for user_id in series_to_users[series_id]:
        matrix_entries[(user_id, episode_id)] += 0.2

  conn_podcast.close()

  return [(u, i, s) for (u, i), s in matrix_entries.iteritems()]


if __name__ == "__main__":
  sc = SparkContext()
  spark = SparkSession(sc)
  redis = RedisConnector('entry_checkpoint')
  connection = redis._single_connect()
  entries = redis.get_dictionary(connection, entry_redis_key)
  if entries is None:
    entries = get_matrix_entries()
    redis.dump_dictionary(connection, {entry_redis_key: entries})
  mat = CoordinateMatrix(sc.parallelize(entries))
