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
import json
from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery as NQuery
import app.constants
import json
import base64

class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        """If input object is an ndarray it will be converted into a dict 
        holding dtype, shape and the data, base64 encoded.
        """
        if isinstance(obj, np.ndarray):
            if obj.flags['C_CONTIGUOUS']:
                obj_data = obj.data
            else:
                cont_obj = np.ascontiguousarray(obj)
                assert(cont_obj.flags['C_CONTIGUOUS'])
                obj_data = cont_obj.data
            data_b64 = base64.b64encode(obj_data)
            return dict(__ndarray__=data_b64,
                        dtype=str(obj.dtype),
                        shape=obj.shape)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder(self, obj)
        
def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct


BUCKET_URL = 'memcached://a3a0672a5043d11e7ae440601bf6be1c-1487269672.us-west-2.elb.amazonaws.com'
@podcastml.route('/', methods=['GET'])
def get_everything():
	n_feats = 5000
	print("RUNNING TFIDF ON %d" % n_feats)
	bucket = Cbucket('couchbase://localhost/podcasts','')
	rConn = RConn(block_size=256)
	rDB = rConn.redisDb
	if (rDB.exists('doc_by_vocab_data')):
		pipe = rDB.pipeline()
		keys = ['doc_by_vocab_data']
		[pipe.get(k) for k in keys]
		result = pipe.execute()
		data = {k:result[i] for i,k in enumerate(keys)}
		doc_by_vocab = rConn.get_numpy('doc_by_vocab','doc_by_vocab_data')
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
		series_episodes = defaultdict(list)
		for e in episodes_dict.values():
			series_episodes[e.seriesTitle].append(e.title)
		# tfidf_vec = TfidfVectorizer(input='context',min_df=10,max_df=0.85,max_features=n_feats,stop_words='english',norm='l2',preprocessor=processText)
		# doc_by_vocab = np.empty([len(episode_index_to_title),n_feats])
		# doc_by_vocab = tfidf_vec.fit_transform([episodes_dict[e].summary for e in episodes_dict]).toarray()

		# index_to_vocab = tfidf_vec.get_feature_names()
		# vocab_to_index = {v:i for i,v in enumerate(index_to_vocab) }
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
		# rDB.set('index_to_vocab',pickle.dumps(index_to_vocab))
		# rDB.set('vocab_to_index',pickle.dumps(vocab_to_index))
		rDB.set('doc_data',pickle.dumps([episodes_dict[e].summary for e in episodes_dict]))
		# rDB.set('doc_by_vocab',pickle.dumps(doc_by_vocab))
		# json.dumps(doc_by_vocab,open("doc_by_vocab.json","w"),cls=NumpyEncoder)
		# key = rConn.store_numpy("doc_by_vocab",doc_by_vocab)
		# rDB.set('doc_by_vocab_data',key)
	return http_resource("nice",'result')
>>>>>>> 4c571c1489af28274b9d664ed62eb2e4005048be

  key_val_pairs = [
    ('e_tags',pickle.dumps(episode_tags)),
    ('s_i_to_t',pickle.dumps(series_index_to_title)),
    ('s_t_to_i',pickle.dumps(series_title_to_index)),
    ('series_episodes',pickle.dumps(series_episodes)),
    ('e_i_to_t',pickle.dumps(episode_index_to_title)),
    ('e_t_to_i',pickle.dumps(episode_title_to_index)),
    ('index_to_vocab',pickle.dumps(index_to_vocab)),
    ('vocab_to_index',pickle.dumps(vocab_to_index))
  ]

	for pair in key_val_pairs:
    redis_db.set(pair[0], pair[1])
    
	key = redis_conn.store_numpy('doc_by_vocab',doc_by_vocab)
	redis_db.set('doc_by_vocab_data',key)

@podcastml.route('/', methods=['GET'])
def get_or_create_redis():
	bucket = Cbucket(constants.COUCHBASE_URL,'')
	redis_conn = RConn(block_size=256)
	redis_db = redis_conn.redisDb
	if (redis_db.exists('doc_by_vocab_data')):
		doc_by_vocab = grab_from_redis(redis_conn, redis_db)
	else:
    populate_redis(redis_conn, redis_db)
		doc_by_vocab = grab_from_redis(redis_conn, redis_db)
	return http_resource(doc_by_vocab.shape,'result')