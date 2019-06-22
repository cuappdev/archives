# Created for PySpark 2.2.0

import os
from collections import defaultdict
import sys

from appdev.connectors import MySQLConnector
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark.mllib.linalg.distributed import CoordinateMatrix

entry_redis_key = 'training_entries'

weights = {
    'recommendations': 0.5,
    'bookmarks': 0.1,
    'listening_histories': 0.2,
    'subscriptions': 0.2
}

def get_matrix_entries(db_u,db_p,db_h,db_n1,db_n2):
  conn = MySQLConnector(db_u,
                        db_p,
                        db_h,
                        db_n1)

  # table name -> (user_id index, episode_id index)
  db_tables = ['recommendations','bookmarks','listening_histories']

  matrix_entries = defaultdict(float)  # (user_id, episode_id) -> score

  for table in db_tables:
    rows = conn.read_batch(table)
    for row in rows:
      # unnecessary int() casting but just in case....
      user_id, episode_id = int(row['user_id']), int(row['episode_id'])
      matrix_entries[(user_id, episode_id)] += weights[table]

  rows = conn.read_batch('subscriptions')
  series_to_users = defaultdict(list)
  for row in rows:
    # unnecessary int() casting but just in case....
    user_id, series_id = int(row['user_id']), int(row['series_id'])
    series_to_users[series_id].append(user_id)

  conn.close()

  conn_podcast = MySQLConnector(db_u,
                                db_p,
                                db_h,
                                db_n2)

  episode_query = 'SELECT id FROM episodes WHERE series_id={}'

  rows = conn_podcast.execute_batch(
      [episode_query.format(series_id) for series_id in series_to_users])
  for (series_id, episode_list) in zip(series_to_users, rows):
    for row in episode_list:
      # unnecessary int() casting but just in case....
      episode_id = int(row['id'])
      for user_id in series_to_users[series_id]:
        matrix_entries[(user_id, episode_id)] += weights['subscriptions']

  conn_podcast.close()

  return [Rating(u, i, s) for (u, i), s in matrix_entries.iteritems()]


if __name__ == "__main__":
  sc = SparkContext()
  spark = SparkSession(sc)
  # redis = RedisConnector('entry_checkpoint')
  # connection = redis._single_connect()
  # entries = redis.get_dictionary(connection, entry_redis_key)
  # if entries is None:
  #   entries = get_matrix_entries()
  #   redis.dump_dictionary(connection, {entry_redis_key: entries})
  print "building ratings"
  arguments = sys.argv
  print arguments
  ratings = sc.parallelize(
      get_matrix_entries(arguments[1],
                         arguments[2],
                         arguments[3],
                         arguments[4],
                         arguments[5]))
  print ratings.take(10)
  print "built ratings"
  rank = int(arguments[6])
  numIterations = int(arguments[7])
  model = ALS.train(ratings, rank, numIterations)
  testdata = ratings.map(lambda p: (p[0], p[1]))
  predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
  ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
  MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
  print "Mean Squared Error = " + str(MSE)
  recommendations = model.recommendProductsForUsers(int(arguments[8]))
  # this needs to be optimized....
  # filtering_set = sc.broadcast(ratings
  #                              .map(lambda r: (r.user, r.product))
  #                              .collect())
  # filtered = recommendations.filter(lambda r: filtering_set.contains((r.user,r.product)))
  def write_to_recommendations(iterator):
    print arguments
    conn_ml = MySQLConnector(arguments[1],
                             arguments[2],
                             arguments[3],
                             arguments[9])
    print "Writing to recommendations"
    conn_ml.write_batch("episodes_for_user", \
    [{'user_id': k, 'episodes_list': ",".join([str(p.product) for p in v])} \
    for (k, v) in iterator])
    conn_ml.close()
  recommendations.foreachPartition(write_to_recommendations)
