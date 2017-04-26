from . import * 
from helpers import http_resource, http_errors,grab_type,top_terms,processText,set_builder
from app.podcastml.models.cbucket import Cbucket
from app.podcastml.models.getrequest import GetRequest
from app.podcastml.models.series import Series
from app.podcastml.models.episode import Episode
from app.podcastml.models.redisconn import RedisConn as RConn

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import redis
import base64
import pickle
from collections import defaultdict

from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery as NQuery
import app.constants

def grab_from_redis(redis_conn, redis_db):
	m = redis_db.hgetall('vocab_to_index')
	pipe = redis_db.pipeline()
	keys = ['doc_by_vocab_data']
	[pipe.get(k) for k in keys]
	result = pipe.execute()
	data = {k:result[i] for i,k in enumerate(keys)}
	key = data['doc_by_vocab_data']
	doc_by_vocab = redis_conn.get_numpy('doc_by_vocab',key)
  return doc_by_vocab

def populate_redis(redis_conn, redis_db):
	series_dict = grab_type(bucket,'series')
	episodes_dict = grab_type(bucket,'episode',series_dict,limit=1000)
	for k in episodes_dict.keys():
		episodes_dict[k].title = episodes_dict[k].title.encode('ascii','ignore')
	series_index_to_title = [series_dict[k].title for k in series_dict.keys()]
	series_title_to_index = {v:i for i,v in enumerate(series_index_to_title) }
	episode_index_to_title = episodes_dict.keys()
	episode_title_to_index = {v:i for i,v in enumerate(episode_index_to_title) }
	series_episodes = defaultdict(list)
	for e in episodes_dict.values():
		series_episodes[e.seriesTitle].append(e.title)
	tfidf_vec = TfidfVectorizer(input='context',min_df=10,max_df=0.85,max_features=n_feats,stop_words='english',norm='l2',preprocessor=processText)
	doc_by_vocab = np.empty([len(episode_index_to_title),n_feats])
	doc_by_vocab = tfidf_vec.fit_transform([episodes_dict[e].summary for e in episodes_dict]).toarray()
	index_to_vocab = tfidf_vec.get_feature_names()
	vocab_to_index = {v:i for i,v in enumerate(index_to_vocab) }
	episode_tags = { e:episodes_dict[e].tags for e in episode_index_to_title}
	index_to_tag = set_builder(episode_tags.values())
	n_tags = len(index_to_tag)
	tag_to_index = {t:i for i,t in enumerate(index_to_tag)}
	episode_tag_matrix = np.zeros([len(episode_index_to_title),n_tags])
	for i in xrange(n_tags):
		for tag in episode_tags[episode_index_to_title[i]]:
			episode_tag_matrix[i][tag_to_index[tag]] = 1

	redis_db.set('e_tags',pickle.dumps(episode_tags))
	redis_db.set('s_i_to_t',pickle.dumps(series_index_to_title))
	redis_db.set('s_t_to_i',pickle.dumps(series_title_to_index))	
	redis_db.set('series_episodes',pickle.dumps(series_episodes))
	redis_db.set('e_i_to_t',pickle.dumps(episode_index_to_title))
	redis_db.set('e_t_to_i',pickle.dumps(episode_title_to_index))
	redis_db.set('index_to_vocab',pickle.dumps(index_to_vocab))
	redis_db.set('vocab_to_index',pickle.dumps(vocab_to_index))
	key = redis_conn.store_numpy('doc_by_vocab',doc_by_vocab)
	redis_db.set('doc_by_vocab_data',key)

@podcastml.route('/', methods=['GET'])
def get_everything():
	n_feats = 15000
	bucket = Cbucket(constants.COUCHBASE_URL,'')
	redis_conn = RConn(block_size=256)
	redis_db = redis_conn.redisDb
	if (redis_db.exists('doc_by_vocab_data')):
		doc_by_vocab = grab_from_redis(redis_conn, redis_db)
	else:
    populate_redis(redis_conn, redis_db)
		doc_by_vocab = grab_from_redis(redis_conn, redis_db)
	return http_resource(doc_by_vocab.shape,'result')