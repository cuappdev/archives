import os

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.linalg.distributed import CoordinateMatrix
from appdev.connectors import MySQLConnector

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

  db_tables = ['recommendations', 'bookmarks', 'listening_histories']

  matrix_entries = {}  # (user_id, episode_id) -> score

  for table in db_tables:
    rows = conn.read_batch(table)
    for row in rows:
      user_id, episode_id = row[3], row[4]
      if (user_id, episode_id) in matrix_entries:
        matrix_entries[(user_id, episode_id)] += weights[table]
      else:
        matrix_entries[(user_id, episode_id)] = weights[table]

  rows = conn.read_batch('subscriptions')
  series_to_users = {}
  for row in rows:
    user_id, series_id = row[3], row[4]
    if series_id in series_to_users:
      series_to_users[series_id].append(user_id)
    else:
      series_to_users[series_id] = [user_id]

  conn.close()

  conn_podcast = MySQLConnector(os.environ['DB_USERNAME'],
                                os.environ['DB_PASSWORD'],
                                os.environ['DB_HOST'],
                                os.environ['PODCAST_DB_NAME'])

  episode_query = 'SELECT id FROM episodes WHERE series_id={}'
  queries = [episode_query.format(series_id) for series_id in series_to_users]

  rows = conn_podcast.execute_batch(queries)
  for (series_id, episode_list) in zip(series_to_users, rows):
    for row in episode_list:
      episode_id = row[0]
      for user_id in series_to_users[series_id]:
        if (user_id, episode_id) in matrix_entries:
          matrix_entries[(user_id, episode_id)] += 0.2
        else:
          matrix_entries[(user_id, episode_id)] = 0.2

  conn_podcast.close()

  return [(u, i, s) for (u, i), s in matrix_entries.iteritems()]


if __name__ == "__main__":
  sc = SparkContext()
  spark = SparkSession(sc)
  entries = sc.parallelize(get_matrix_entries())
  mat = CoordinateMatrix(entries)
