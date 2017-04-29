# Methods to compose HTTP response JSON 
from flask import jsonify
from app.podcastml.models.cbucket import Cbucket
from app.podcastml.models.getrequest import GetRequest
from app.podcastml.models.series import Series
from app.podcastml.models.episode import Episode
from app.podcastml.models.matrix import Matrix
from bs4 import BeautifulSoup
import numpy as np

from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery as NQuery

def http_json(result, bool):
	result.update({ "success": bool })
	return jsonify(result)


def http_resource(result, name, bool=True):
	resp = { "data": { name : result }}
	return http_json(resp, bool)


def http_errors(result): 
	errors = { "data" : { "errors" : result.errors["_schema"] }}
	return http_json(errors, False)

def grab_type(bucket,input_type,series_dict={},limit=100):
	e_bool = False
	if input_type=="episode":
		e_bool = True
	episodes = {}
	offset = 0
	if series_dict:
		series_keys = series_dict.keys()
	while True:
		result = GetRequest().get_query(bucket,"select * from podcasts WHERE type=\"" + input_type + "\" ",limit,offset)
		if result.get_single_result() == None:
			break
		for row in result:
			r = row['podcasts']
			if e_bool:
				if r['seriesId'] in series_keys:
					episodes[r['title'].encode('ascii','ignore')] = Episode(series_dict[r['seriesId']],r['title'],r['author'],r['summary'],r['pubDate'],r['duration'],[t.encode('ascii','ignore').replace("\"","") for t in r['tags']],r['audioUrl'])
			else:
				series_dict[int(r['id'])] = Series(r['id'], r['author'], r['country'], r['author'], r['imageUrlSm'], r['imageUrlLg'], r['feedUrl'], r['genres'])
		offset+=1
	return episodes if e_bool else series_dict
	
def top_terms(n1, n2,doc_by_vocab,index_to_vocab,episode_name_to_index,k=10):
    e1 = doc_by_vocab[episode_name_to_index[n1]]
    e2 = doc_by_vocab[episode_name_to_index[n2]]
    result = [index_to_vocab[key] for key in np.multiply(e1,e2).argsort()[-k:][::-1]]
    return result

def top_similair(e,e_sims,episode_index_to_name,episode_name_to_index,k=10):
	e_index = episode_name_to_index[e]
	print(e)
	print("=======")
	filtered_s = e_sims[e_index].argsort()[-(k+1):][::-1]
	return [episode_index_to_name[i] for i in filtered_s if key!= e_index]

def from_numpy_matrix(name,mat):
	"""
	    Creates a matrix from a numpy matrix
	"""
	if len(mat.shape) != 2:
	    raise BaseException('Shape of input matrix must be of size 2')
	rows = mat.shape[0]
	cols = mat.shape[1]
	Matrix('doc_by_vocab', rows, cols,rDB,block_size=256)	
	m = Matrix(rows, cols, name,)
	# Separate blocks and send them to the redis server
	for j in range(0, m.row_blocks()):
	    for i in range(0, m.col_blocks()):
	        block_name = m.block_name(j,i)
	        block = mat[max(j*context.block_size,0):min((j+1)*context.block_size,rows+1),
	                    max(i*context.block_size,0):min((i+1)*context.block_size,cols+1)]
	        
	        redwrap.create_block(block_name, block)
	return m

def processText(s):
	return BeautifulSoup(s,"html.parser").text

def set_builder(lst):
	output = []
	for l in lst:
		output+=list(set(l))
	return list(set(output))