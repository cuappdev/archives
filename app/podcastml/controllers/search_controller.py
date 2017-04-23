from . import * 
from helpers import http_resource, http_errors,grab_type,top_terms,processText,set_builder
from app.podcastml.models.cbucket import Cbucket
from app.podcastml.models.getrequest import GetRequest
from app.podcastml.models.series import Series
from app.podcastml.models.episode import Episode
from app.podcastml.models.redisconn import RedisConn as RConn
####
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import redis
import base64
import pickle
from collections import defaultdict
####
# from IPython.parallel import Client
####
from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery as NQuery

BUCKET_URL = 'memcached://a3a0672a5043d11e7ae440601bf6be1c-1487269672.us-west-2.elb.amazonaws.com'
@podcastml.route('/', methods=['GET'])
def get_everything():
	n_feats = 15000
	print("RUNNING TFIDF ON %d" % n_feats)
	bucket = Cbucket('couchbase://localhost/podcasts','')
	rConn = RConn(block_size=256)
	rDB = rConn.redisDb
	if (rDB.exists('doc_by_vocab_data')):
		m = rDB.hgetall('vocab_to_index')
		pipe = rDB.pipeline()
		keys = ['doc_by_vocab_data']
		[pipe.get(k) for k in keys]
		result = pipe.execute()
		data = {k:result[i] for i,k in enumerate(keys)}
		key = data['doc_by_vocab_data']
		doc_by_vocab = rConn.get_numpy('doc_by_vocab',key)
		print(doc_by_vocab.shape)
	else:
		series_dict = grab_type(bucket,'series')
		episodes_dict = grab_type(bucket,'episode',series_dict,limit=1000)
		for k in episodes_dict.keys():
			episodes_dict[k].title = episodes_dict[k].title.encode('ascii','ignore')
		series_index_to_title = [series_dict[k].title for k in series_dict.keys()]
		series_title_to_index = {v:i for i,v in enumerate(series_index_to_title) }
		episode_index_to_title = episodes_dict.keys()
		episode_title_to_index = {v:i for i,v in enumerate(episode_index_to_title) }
		print episodes_dict['68: Millionaire Interview: Melanie Duncan, Entrepreneur, Designer, Philosopher, and World-Traveler'].summary
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

		rDB.set('e_tags',pickle.dumps(episode_tags))
		rDB.set('s_i_to_t',pickle.dumps(series_index_to_title))
		rDB.set('s_t_to_i',pickle.dumps(series_title_to_index))	
		rDB.set('series_episodes',pickle.dumps(series_episodes))
		rDB.set('e_i_to_t',pickle.dumps(episode_index_to_title))
		rDB.set('e_t_to_i',pickle.dumps(episode_title_to_index))
		rDB.set('index_to_vocab',pickle.dumps(index_to_vocab))
		rDB.set('vocab_to_index',pickle.dumps(vocab_to_index))
		key = rConn.store_numpy('doc_by_vocab',doc_by_vocab)
		print(key)
		rDB.set('doc_by_vocab_data',key)
	return http_resource(doc_by_vocab.shape,'result')


