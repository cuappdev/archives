#### Flask Imports
from . import * 
from flask import request
####
#### Helper Methods
from helpers import http_resource, http_errors, processText, set_builder
####
#### Model Imports

from app.podcastml.models.cbucket import Cbucket
from app.podcastml.models.getrequest import GetRequest
from app.podcastml.models.series import Series
from app.podcastml.models.episode import Episode
from app.podcastml.models.redisconn import RedisConn as RConn

from app.podcastml.models.contentBasedNet import CBN
####
#### NLP IR ML and Redis Imports
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds

import numpy as np
import redis
import base64
import pickle
from collections import defaultdict
import json
from log import logger
import os
####
# from IPython.parallel import Client
#### Couchbase
from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery as NQuery
import h5py
import json
import base64

@podcastml.route('/', methods=['GET'])
def hello_world():
	"""
	This is a hello world endpoint

	@return json: "hello world"
	"""
	logger.info('This is hello world')
	return http_resource("Hello World",'result')

@podcastml.route('/topics', methods=['GET'])
def run_topic_model():
    """
    Runs the topic model.
    """
    series = podcast_bucket.get_series()
    episodes = podcast_bucket.get_episodes(series_dict=series,limit=20000)
    t = TopicModel(episodes=episodes, series=series, n_tags=100)
    # TODO run
    return

@podcastml.route('dump', methods=['GET'])
def preprocessing():
	arguments = request.args
	if 'n_feats' in arguments:
		n_feats = int(arguments['n_feats'])
	else:
		n_feats = 5000
	logger.info('Running on %d features' % n_feats)
	podcast_bucket = Cbucket(os.environ["BUCKET_URL"]+"/podcasts",'')
	logger.info('Connected to CouchBase')
	rConn = RConn(name='podcastML',host='localhost', port=6379, db=0,max_execs=3,timeout=10,block_size=256,slave_number=2)
	rDB = rConn.redisDb
	logger.info('Connected to Redis Connector')
	logger.info('Collecting Series')
	series = podcast_bucket.get_series()
	logger.info('Finished Collecting Series')
	logger.info('Collecting Episodes')
	episodes = podcast_bucket.get_episodes(series_dict=series,limit=20000)
	logger.info('Finished Collecting Episodes')
	logger.info('Creating series_index_to_title')
	series_index_to_title = [series[k].title for k in series.keys()]
	logger.info('Finished Creating series_index_to_title')
	logger.info('Creating series_title_to_index')
	series_title_to_index = {v:i for i,v in enumerate(series_index_to_title)}
	logger.info('Finished Creating series_title_to_index')
	logger.info('Creating episode_index_to_title')
	episode_index_to_title = episodes.keys()
	logger.info('Finished Creating episode_index_to_title')
	logger.info('Creating episode_title_to_index')
	episode_title_to_index = {v:i for i,v in enumerate(episode_index_to_title) }
	logger.info('Finished Creating episode_title_to_index')
	logger.info('Creating episode_processed_summaries')
	episode_processed_summaries = [processText(episodes[e].summary) for e in episodes]
	logger.info('Finished Creating episode_processed_summaries')
	tfidf_vec = TfidfVectorizer(input='context',min_df=10,max_df=0.85,max_features=n_feats,stop_words='english',norm='l2')
	logger.info('Vectorizing episodes')
	doc_by_vocab = np.empty([len(episode_index_to_title),n_feats])
	doc_by_vocab = tfidf_vec.fit_transform(episode_processed_summaries).toarray()
	logger.info('Finished Vectorizing episodes')
	logger.info('Creating index_to_vocab')
	index_to_vocab = tfidf_vec.get_feature_names()
	logger.info('Finished Creating index_to_vocab')
	logger.info('Creating vocab_to_index')
	vocab_to_index = {v:i for i,v in enumerate(index_to_vocab)}
	logger.info('Finished Creating vocab_to_index')
	logger.info('Creating episode_tags')
	episode_tags = { e:episodes[e].tags for e in episode_index_to_title}
	logger.info('Finished Creating episode_tags')
	logger.info('Creating index_to_tag')
	index_to_tag = set_builder(episode_tags.values())
	logger.info('Finished Creating index_to_tag')
	n_tags = len(index_to_tag)
	logger.info('Creating tag_to_index')
	tag_to_index = {t:i for i,t in enumerate(index_to_tag)}
	logger.info('Finished Creating tag_to_index')
	logger.info('Applying SVD on TFIDF')
	u, s, v_trans = svds(doc_by_vocab, k=100)
	logger.info('Finished applying SVD')
	logger.info('Dumping into Redis')
	h5f = h5py.File('u.hdf5', 'w', driver='core', backing_store=False)
	doc_compressed = h5f.create_dataset("doc_compressed",data=u)
	h5f.close()


	# else:
	# 	series_dict = grab_type(bucket,'series')
	# 	episodes_dict = grab_type(bucket,'episode',series_dict,limit=1000)
	# 	for k in episodes_dict.keys():
	# 		episodes_dict[k].title = episodes_dict[k].title.encode('ascii','ignore')
	# 	series_index_to_title = [series_dict[k].title for k in series_dict.keys()]
	# 	series_title_to_index = {v:i for i,v in enumerate(series_index_to_title) }
	# 	episode_index_to_title = episodes_dict.keys()
	# 	episode_title_to_index = {v:i for i,v in enumerate(episode_index_to_title) }
	# 	series_episodes = defaultdict(list)
	# 	for e in episodes_dict.values():
	# 		series_episodes[e.seriesTitle].append(e.title)
	# 	tfidf_vec = TfidfVectorizer(input='context',min_df=10,max_df=0.85,max_features=n_feats,stop_words='english',norm='l2',preprocessor=processText)
	# 	doc_by_vocab = np.empty([len(episode_index_to_title),n_feats])
	# 	doc_by_vocab = tfidf_vec.fit_transform([episodes_dict[e].summary for e in episodes_dict]).toarray()

	# 	index_to_vocab = tfidf_vec.get_feature_names()
	# 	vocab_to_index = {v:i for i,v in enumerate(index_to_vocab) }
	# 	episode_tags = { e:episodes_dict[e].tags for e in episode_index_to_title}
	# 	index_to_tag = set_builder(episode_tags.values())
	# 	n_tags = len(index_to_tag)
	# 	tag_to_index = {t:i for i,t in enumerate(index_to_tag)}
	# 	episode_tag_matrix = np.zeros([len(episode_index_to_title),n_tags])
	# 	for i in xrange(n_tags):
	# 		for tag in episode_tags[episode_index_to_title[i]]:
	# 			episode_tag_matrix[i][tag_to_index[tag]] = 1
	# 	rDB.set('e_tags',pickle.dumps(episode_tags))
	# 	rDB.set('s_i_to_t',pickle.dumps(series_index_to_title))
	# 	rDB.set('s_t_to_i',pickle.dumps(series_title_to_index))	
	# 	rDB.set('series_episodes',pickle.dumps(series_episodes))
	# 	rDB.set('e_i_to_t',pickle.dumps(episode_index_to_title))
	# 	rDB.set('e_t_to_i',pickle.dumps(episode_title_to_index))
	# 	# rDB.set('index_to_vocab',pickle.dumps(index_to_vocab))
	# 	# rDB.set('vocab_to_index',pickle.dumps(vocab_to_index))
	# 	rDB.set('doc_data',pickle.dumps([episodes_dict[e].summary for e in episodes_dict]))
	# 	rDB.set('doc_by_vocab',pickle.dumps(doc_by_vocab))
	# 	json.dumps(doc_by_vocab,open("doc_by_vocab.json","w"),cls=NumpyEncoder)
	# 	key = rConn.store_numpy("doc_by_vocab",doc_by_vocab)
	# 	rDB.set('doc_by_vocab_data',key)
	return http_resource("nice",'result')