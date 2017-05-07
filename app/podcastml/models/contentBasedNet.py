#### Keras Imports
from keras.layers import Dense, Input, Embedding, Flatten, Lambda
from keras.models import Model
from keras.layers.merge import dot
import keras.backend as K
####
#### Logging Imports
import log
####


class CBN(object):
  """
    Content Based Network v1

    This is a network that is order INSENSITVE that leverages TFIDF vectors
    For this model, I will specifically be applying SVDs on the TFIDF vectors
    to denoise via dimensionality reduction. I then input these vectors into the 
    neural net for prediction. The net has a single dense layer and a dot product
    layer. I optimize the net with ADAM and minimize the loss using MAE of the mean 
    squared error between the predicted score and the label.
  """

  def __init__(self, users,user_indeces,ratings,meta_features,labels,embed_dim=5,num_epocs=5,batch_size=32,collab_filter=False):
    """ Constructor """
    self.users 			    = users
    self.user_indeces       = user_indeces
    self.n_users            = len(user_indeces)
    self.ratings            = ratings 
    self.meta_features      = meta_features 
    self.num_meta           = meta_features.shape[1]
    self.labels             = labels
    self.embed_dim 			= embed_dim
    self.batch_size         = batch_size
    self.collab_filter	    = collab_filter
    self.num_epocs          = num_epocs
    self.model              = self.create_fitted_model()
    self.logger             = log.logger

  def create_fitted_model(self,single_user=True):
    """
    This CBN fits on a list of users, meta features which are just TFIDF values
    taken from the summary, the rankings from the entire user base
    on each document instance, and labels which are just zeroes. 
    The goal of the system is just to minimize the error and bring it as close
    to zero as possible. As such, our labels are zero and our training model
    is trying to minimize the error between the "error":output  and "zero":label

    @param: user_in: np.array() of user index
    @param: meta_features_in: np.array() with float features of text data
    @param: ratings: np.array() of ratings matrix
    @param: labels: np.array() with just zeroes intially

    @returns: test model with trained layers
    """
    user_in = Input((1,), dtype = 'int32')
    meta_features_in = Input((self.meta_features.shape[1],), dtype = 'float32')
    true_rating_in = Input((1,), dtype = 'float32')

    user_embeddings = Embedding(self.n_users, self.embed_dim)
    user_encoded = Flatten()(user_embeddings(user_in))

    episode_encoded = Dense(self.embed_dim)(meta_features_in)
    prediction = dot([user_encoded, episode_encoded], axes = 1)
    error = Lambda(lambda x: K.mean(K.square(x[0] - x[1]), axis=-1, keepdims = True))
    model = Model(inputs = [user_in, meta_features_in,true_rating_in],
                         outputs = error([prediction, true_rating_in]))
    model.compile(loss = 'mae', optimizer = 'adam', metrics=['accuracy','loss'])
    self.logger.info('Compiled model and beginning fitting')
    if single_user:
        model.fit([self.users,self.meta_features,self.ratings],labels,validation_split = .1,epochs=self.num_epocs,verbose=0)
    else:
        for epoch in range(self.num_epocs):
            self.logger.info('Starting epoch %d of %d' % (epoch,self.num_epocs))
            for i,u_id in enumerate(self.user_indeces):
                model.train_on_batch([float(u_id)/self.n_users,self.meta_features,ratings[i]],labels)
            self.logger.info('Finished epoch %d of %d' % (epoch,self.num_epocs))    
    self.logger.info('Finished fitting model')  
    self.logger.info('Created test model')
    test_model = Model(inputs = [user_in, meta_features_in],
                         outputs = [prediction])
    self.logger.info('Finished test model')
    return test_model

  def predict(self,u_in,meta_in):
    """
    This is the preidction function.

    @param: int: user index in rating matrix
    @param  np.array: meta_features

    @returns: score
    """
    return self.model.predict([np.array([float(u_in)/(self.n_users+1)]),meta_in.reshape(1,self.num_meta)], batch_size=32)