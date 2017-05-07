import pickle
import numpy as np
from scipy.sparse import csr_matrix

class BaseRecommender(object):
    def recommend_episodes(self,dataset,u,max_episodes=10,return_scores=True,episode_features=None):
        """
        Recommend new episodes for a user.
        Parameters
        ==========
        dataset : scipy.sparse.csr_matrix
            User-episode matrix containing known episodes.
        u : int
            Index of user for which to make recommendations.
        max_episodes : int
            Maximum number of recommended episodes to return.
        return_scores : bool
            If true return a score along with each recommended episode.
        episode_features : array_like, shape = [num_episodes, num_features]
        Returns
        =======
        recs : list
            List of (idx,score) pairs if return_scores is True, else
            just a list of idxs.
        """
        raise NotImplementedError('you must implement recommend_episodes()')

    def fit(self,train,episode_features=None):
        """
        Train on supplied data. In general you will want to
        implement this rather than computing recommendations on
        the fly.
        Parameters
        ==========
        train : scipy.sparse.csr_matrix or mrec.sparse.fast_sparse_matrix, shape = [num_users, num_episodes]
            User-episode matrix.
        episode_features : array_like, shape = [num_episodes, num_features]
            Features for episodes in training set, required by some recommenders.
        """
        raise NotImplementedError('you should implement fit()')

    def save(self,filepath):
        """
        Serialize model to file.
        Parameters
        ==========
        filepath : str
            Filepath to write to, which must have the '.npz' suffix.
        Notes
        =====
        Internally numpy.savez may be used to serialize the model and
        this would add the '.npz' suffix to the supplied filepath if
        it were not already present, which would most likely cause errors
        in client code.
        """
        if not filepath.endswith('.npz'):
            raise ValueError('invalid filepath {0}, must have ".npz" suffix'.format(filepath))

        archive = self._create_archive()
        if archive:
            np.savez(filepath,**archive)
        else:
            pickle.dump(self,open(filepath,'w'))

    @staticmethod
    def load(filepath):
        """
        Load a recommender model from file after it has been serialized with
        save().
        Parameters
        ==========
        filepath : str
            The filepath to read from.
        """
        r = np.load(filepath)
        if isinstance(r,BaseRecommender):
            model = r
        else:
            model = np.loads(str(r['model']))
            model._load_archive(r)  # restore any fields serialized separately
        return model

    def batch_recommend_episodes(self,
                              dataset,
                              max_episodes=10,
                              return_scores=True,
                              show_progress=False,
                              episode_features=None):
        """
        Recommend new episodes for all users in the training dataset.
        Parameters
        ==========
        dataset : scipy.sparse.csr_matrix
            User-episode matrix containing known episodes.
        max_episodes : int
            Maximum number of recommended episodes to return.
        return_scores : bool
            If true return a score along with each recommended episode.
        show_progress: bool
            If true print something to stdout to show progress.
        episode_features : array_like, shape = [num_episodes, num_features]
            Optionally supply features for each episode in the dataset.
        Returns
        =======
        recs : list of lists
            Each entry is a list of (idx,score) pairs if return_scores is True,
            else just a list of idxs.
        Notes
        =====
        This provides a default implementation, you will be able to optimize
        this for most recommenders.
        """
        recs = []
        for u in xrange(self.num_users):
            if show_progress and u%1000 == 0:
               print u,'..',
            recs.append(self.recommend_episodes(dataset,u,max_episodes,return_scores))
        if show_progress:
            print
        return recs

    def range_recommend_episodes(self,
                              dataset,
                              user_start,
                              user_end,
                              max_episodes=10,
                              return_scores=True,
                              episode_features=None):
        """
        Recommend new episodes for a range of users in the training dataset.
        Parameters
        ==========
        dataset : scipy.sparse.csr_matrix
            User-episode matrix containing known episodes.
        user_start : int
            Index of first user in the range to recommend.
        user_end : int
            Index one beyond last user in the range to recommend.
        max_episodes : int
            Maximum number of recommended episodes to return.
        return_scores : bool
            If true return a score along with each recommended episode.
        episode_features : array_like, shape = [num_episodes, num_features]
            Optionally supply features for each episode in the dataset.
        Returns
        =======
        recs : list of lists
            Each entry is a list of (idx,score) pairs if return_scores is True,
            else just a list of idxs.
        Notes
        =====
        This provides a default implementation, you will be able to optimize
        this for most recommenders.
        """
        return [self.recommend_episodes(dataset,u,max_episodes,return_scores) for u in xrange(user_start,user_end)]

    def _zero_known_episode_scores(self,r,train):
        """
        Helper function to set predicted scores/ratings for training episodes
        to zero or less, to avoid recommending already known episodes.
        Parameters
        ==========
        r : numpy.ndarray or scipy.sparse.csr_matrix
            Predicted scores/ratings.
        train : scipy.sparse.csr_matrix
            The training user-episode matrix, which can include zero-valued entries.
        Returns
        =======
        r_safe : scipy.sparse.csr_matrix
            r_safe is equal to r except that r[u,i] <= 0 for all u,i with entries
            in train.
        """
        col = train.indices
        if isinstance(r,csr_matrix):
            max_score = r.data.max()
        else:
            max_score = r.max()
        data = max_score * np.ones(col.shape)
        # build up the row (user) indices
        # - we can't just use row,col = train.nonzero() as this eliminates
        #   u,i for which train[u,i] has been explicitly set to zero
        row = np.zeros(col.shape)
        for u in xrange(train.shape[0]):
            start,end = train.indptr[u],train.indptr[u+1]
            if end > start:
                row[start:end] = u
        return r - csr_matrix((data,(row,col)),shape=r.shape)
