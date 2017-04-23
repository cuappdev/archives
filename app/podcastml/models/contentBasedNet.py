from keras.layers import Dense, Input, Embedding, Flatten
from keras.models import Model
from keras.layers.merge import dot
from keras.losses import mean_squared_error

class CBN(object):
  """Content Based Network"""

  def __init__(self, n_user,n_episodes,n_meta_features,embed_dim=5,collab_filter=False):
    """Constructor"""
    self.n_user 			= n_user
    self.n_episodes    = n_episodes 
    self.n_meta_features   		= n_meta_features 
    self.embed_dim 			= embed_dim
    self.collab_filter	= collab_filter
    self.model = self.create_model()

  def create_model(self):
    user_in = Input((1,), dtype = 'int32')
    true_rating_in = Input((1,), dtype = 'float32')
    meta_features_in = Input((self.n_meta_features,), dtype = 'float32')
    user_embeddings = Embedding(self.n_user, self.embed_dim)
    user_encoded = Flatten()(user_embeddings(user_in))
    episode_encoded = Dense(self.embed_dim)(meta_features_in)
    prediction = dot([user_encoded, episode_encoded], axes = 1)
    model = Model(inputs = [user_in, meta_features_in, true_rating_in],
                     outputs = prediction)
    model.compile(loss = 'mse', optimizer = 'adam')
    model.summary()
    return model

  def train_model(self,training_data):
    pass

  def predict(self,user_in,meta_features_in):
    pass
