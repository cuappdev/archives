import redis
import time 
import numpy as np
from app.podcastml.models.matrix import Matrix

class RedisConn(object):
  """Redis Connection object"""

  def __init__(self, name='ilan_server',host='localhost', port=6379, db=0,max_execs=3,timeout=10,block_size=256,slave_number=2):
    """Constructor"""
    self.name 			= name
    self.host        	= host 
    self.port   		= port 
    self.db 			= db
    self.max_execs	= max_execs
    self.timeout	= timeout
    self.block_size	= block_size
    self.slave_number	= slave_number
    self.redisDb        = self._connect_rd()
    self.rPool			= self._connect_pool()

  def _connect_rd(self):
    """Connect to the DB"""
    return redis.Redis(host=self.host,port=self.port,db=self.db)

  def _connect_pool(self):
  	pool = redis.ConnectionPool(host=self.host,port=self.port,db=self.db)
  	return redis.Redis(connection_pool=pool)

  def _create_server(self):
  	data = {}
  	data['server_name'] = self.name
  	data['jobs'] = {'max_execs': self.max_execs,'timeout':self.timeout}
  	data['matrix'] = {'block_size': self.block_size}
  	data['redis_master'] = {'host':self.host,'port':self.port,'db':self.db}
  	data['redis_slaves'] = {}
  	for c in range(self.slave_number-self.db-1):
  		data['redis_slaves']['slave'+str(c)] = {'host':self.host,'port':self.port,'db':self.db+c}
  	return server.Server(data)

  def store_numpy(self,name,mat):
    """
      Creates a matrix from a numpy matrix
    """
    if len(mat.shape) != 2:
        raise BaseException('Shape of input matrix must be of size 2')
    rows,cols = mat.shape
    array_dtype = str(mat.dtype)
    m = mat.ravel().tostring()
    key = '{0}|{1}#{2}#{3}'.format(int(time.time()), array_dtype, rows, cols)
    self.redisDb.set(name,m)
    return key

  def get_numpy(self,name,key):
    d_mat = self.redisDb.get(name)
    array_dtype, row, col = key.split('|')[1].split('#')
    return np.fromstring(d_mat, dtype=array_dtype).reshape(int(row), int(col))