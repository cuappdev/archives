# cython: cdivision=True
# cython: boundscheck=False

cimport numpy as np

import numpy as np
import scipy

cdef extern from "stdlib.h":
    int rand() nogil

cdef extern from "math.h":
    double sqrt(double x) nogil

def warp_sample(np.ndarray[np.float_t,ndim=2] U,
                np.ndarray[np.float_t,ndim=2] V,
                np.ndarray[np.float_t,ndim=1] vals,
                np.ndarray[np.int32_t,ndim=1] indices,
                np.ndarray[np.int32_t,ndim=1] indptr,
                positive_thresh,
                max_trials):
    """
    Sample a user and a violating pair of positive and negative (lower- or un-rated)
    episodes given the current user and episode factors.

    Parameters
    ==========
    U : numpy.ndarray
        User factors.
    V : numpy.ndarray
        episode factors.
    vals : numpy.ndarray
        Rating values.
    indices : numpy.ndarray
        Corresponding episode indices.
    indptr : numpy.ndarray
        Corresponding pointers into indices for episodes for each user,
        so vals,indices,indptr = train.data,train.indices,train.indptr
        assuming train is a scipy.sparse.csr_matrix of ratings.
    positive_thresh: float
        Consider an episode to be "positive" i.e. liked if its rating is at least this.
    max_trials : int
        Resample user and positive episode if we can't find a violating negative example
        within this many attempts.

    Returns
    =======
    u : int
        Sampled user.
    i : int
        Sampled positive episode.
    j : int
        Sampled negative episode.
    N : int
        Number of negative episodes that had to be sampled to find a violating one.
    tot_trials : int
        Total number of trials taken to find a sample.
    """

    cdef unsigned int num_users, u, ix, i, N, tot_trials
    cdef int j

    num_users = U.shape[0]
    tot_trials = 0

    while True:
        u,ix,i = sample_positive_example(positive_thresh,num_users,vals,indices,indptr)
        j,N = sample_violating_negative_example(U,V,vals,indices,indptr[u],indptr[u+1],u,ix,i,max_trials)
        tot_trials += N
        if j >= 0:
            return u,i,j,N,tot_trials

cdef sample_violating_negative_example(np.ndarray[np.float_t,ndim=2] U,
                                        np.ndarray[np.float_t,ndim=2] V,
                                        np.ndarray[np.float_t,ndim=1] vals,
                                        np.ndarray[np.int32_t,ndim=1] indices,
                                        begin,
                                        end,
                                        u,
                                        ix,
                                        i,
                                        max_trials):
    """
    Sample a violating negative episode given the current episode and user factors.

    Parameters
    ==========
    U : numpy.ndarray
        User factors.
    V : numpy.ndarray
        episode factors.
    vals : numpy.ndarray
        Rating values.
    indices : numpy.ndarray
        Corresponding episode indices.
    begin : int
        Start index into vals and indices for possible negative episode.
    end : int
        End index into vals and inidices for possible negative episode.
    u : int
        The sample user.
    ix : int
        Index into vals and indices for the positive episode.
    i : int
        The sample positive episode.
    max_trials : int
        Give up if we can't find a violating example within this many attempts.

    Returns
    =======
    j : int
        Sampled negative episode or -1 if no violating episode could be found.
    N : int
        Number of negative episodes that had to be sampled to find a violating one.
    """

    cdef float r
    cdef unsigned int N, num_episodes
    cdef int j

    num_episodes = V.shape[0]

    r = U[u].dot(V[i])
    for N in xrange(1,max_trials):
        # find j!=i s.t. data[u,j] < data[u,i]
        j = sample_negative_example(num_episodes,vals,indices,begin,end,ix)
        if r - U[u].dot(V[j]) < 1:
            # found a violating pair
            return j,N
    # no violating pair found after max_trials, give up
    return -1,max_trials

cdef sample_negative_example(num_episodes,
                             np.ndarray[np.float_t,ndim=1] vals,
                             np.ndarray[np.int32_t,ndim=1] indices,
                             begin,
                             end,
                             ix):
    """
    Sample a negative (lower- or un-rated) episode given a positive episode.

    Parameters
    ==========
    num_episodes : int
        Total number of episodes.
    vals : numpy.ndarray
        Rating values.
    indices : numpy.ndarray
        Corresponding episode indices.
    begin : int
        Start index into vals and indices for possible negative episode.
    end : int
        End index into vals and inidices for possible negative episode.
    ix : int
        Index into vals and indices for the positive episode.

    Returns
    =======
    j : int
        Sampled negative episode.
    """

    cdef unsigned int j, jx, found

    while True:
        # sample episode uniformly with replacement
        j = rand() % num_episodes
        found = 0
        for jx in xrange(begin,end):
            if indices[jx] == j:
                found = 1
                break
        if not found or vals[jx] < vals[ix]:
            return j

cdef sample_positive_example(positive_thresh,
                             num_users,
                             np.ndarray[np.float_t,ndim=1] vals,
                             np.ndarray[np.int32_t,ndim=1] indices,
                             np.ndarray[np.int32_t,ndim=1] indptr):
    """
    Uniformly sample a user and one of their positive episodes.
    Note this doesn't really sample users uniformly: they will
    get sampled more often if they have a high proportion of
    positive episodes.

    Parameters
    ==========
    positive_thresh: float
        Consider an episode to be "positive" i.e. liked if its rating is at least this.
    num_users : int
        The total number of users.
    vals : numpy.ndarray
        Rating values.
    indices : numpy.ndarray
        Corresponding episode indices.
    indptr : numpy.ndarray
        Corresponding pointers into indices for episodes for each user,
        so vals,indices,indptr = train.data,train.indices,train.indptr
        assuming train is a scipy.sparse.csr_matrix of ratings.
    """

    cdef unsigned int u, i, ix, begin, end

    while True:
        # pick a random user
        u = rand() % num_users
        begin = indptr[u]
        end = indptr[u+1]
        if end > begin:
            # pick one of their positive episodes
            ix = begin + (rand() % (end-begin))
            if vals[ix] >= positive_thresh:
                i = indices[ix]
                return u,ix,i

def apply_updates(np.ndarray[np.float_t,ndim=2] F,
                  np.ndarray[np.int32_t,ndim=1] rows,
                  np.ndarray[np.float_t,ndim=2] deltas,
                  gamma,
                  C):
    """
    Apply SGD updates.

    Parameters
    ==========
    F : numpy.ndarray
        The factors to be updated.
    rows : numpy.ndarray
        Vector of row indices for which we have updates.
    deltas : numpy.ndarray
        Matrix of updates.
    gamma : float
        The learning rate.
    C : float
        The regularization constant.
    """
 
    cdef unsigned int i, num
    cdef float p

    assert(rows.shape[0] == deltas.shape[0])

    num = rows.shape[0]
    for i in xrange(num):
        row = rows[i]
        delta = deltas[i]
        F[row] += gamma*delta
        p = sqrt(F[row].T.dot(F[row]))/C
        if p > 1:
            F[row] /= p  # ensure ||F[row]|| <= C

def warp2_sample(np.ndarray[np.float_t,ndim=2] U,
                np.ndarray[np.float_t,ndim=2] V,
                np.ndarray[np.float_t,ndim=2] W,
                X,
                np.ndarray[np.float_t,ndim=1] vals,
                np.ndarray[np.int32_t,ndim=1] indices,
                np.ndarray[np.int32_t,ndim=1] indptr,
                positive_thresh,
                max_trials):
    """
    Sample a user and a violating pair of positive and negative (lower- or un-rated)
    episodes given the current user, episode and feature factors.

    Parameters
    ==========
    U : numpy.ndarray
        User factors.
    V : numpy.ndarray
        episode factors.
    W : numpy.ndarray
        episode feature factors.
    X : numpy.ndarray
        episode features.
    vals : numpy.ndarray
        Rating values.
    indices : numpy.ndarray
        Corresponding episode indices.
    indptr : numpy.ndarray
        Corresponding pointers into indices for episodes for each user,
        so vals,indices,indptr = train.data,train.indices,train.indptr
        assuming train is a scipy.sparse.csr_matrix of ratings.
    positive_thresh: float
        Consider an episode to be "positive" i.e. liked if its rating is at least this.
    max_trials : int
        Resample user and positive episode if we can't find a violating negative example
        within this many attempts.

    Returns
    =======
    u : int
        Sampled user.
    i : int
        Sampled positive episode.
    j : int
        Sampled negative episode.
    N : int
        Number of negative episodes that had to be sampled to find a violating one.
    tot_trials : int
        Total number of trials taken to find a sample.
    """

    cdef unsigned int num_users, u, ix, i, N, tot_trials
    cdef int j

    num_users = U.shape[0]
    tot_trials = 0

    while True:
        u,ix,i = sample_positive_example(positive_thresh,num_users,vals,indices,indptr)
        j,N = sample_violating_negative_example2(U,V,W,X,vals,indices,indptr[u],indptr[u+1],u,ix,i,max_trials)
        tot_trials += N
        if j >= 0:
            return u,i,j,N,tot_trials

cdef sample_violating_negative_example2(np.ndarray[np.float_t,ndim=2] U,
                                        np.ndarray[np.float_t,ndim=2] V,
                                        np.ndarray[np.float_t,ndim=2] W,
                                        X,
                                        np.ndarray[np.float_t,ndim=1] vals,
                                        np.ndarray[np.int32_t,ndim=1] indices,
                                        begin,
                                        end,
                                        u,
                                        ix,
                                        i,
                                        max_trials):
    """
    Sample a violating negative episode given the current episode and user factors.

    Parameters
    ==========
    U : numpy.ndarray
        User factors.
    V : numpy.ndarray
        episode factors.
    W : numpy.ndarray
        episode feature factors.
    X : numpy.ndarray
        episode features.
    vals : numpy.ndarray
        Rating values.
    indices : numpy.ndarray
        Corresponding episode indices.
    begin : int
        Start index into vals and indices for possible negative episode.
    end : int
        End index into vals and inidices for possible negative episode.
    u : int
        The sample user.
    ix : int
        Index into vals and indices for the positive episode.
    i : int
        The sample positive episode.
    max_trials : int
        Give up if we can't find a violating example within this many attempts.

    Returns
    =======
    j : int
        Sampled negative episode or -1 if no violating episode could be found.
    N : int
        Number of negative episodes that had to be sampled to find a violating one.
    """

    cdef float r
    cdef unsigned int N, num_episodes
    cdef int j
    cdef np.ndarray[np.float_t,ndim=1] XW
    cdef np.ndarray[np.float_t,ndim=1] xbuf

    num_episodes = V.shape[0]
    is_sparse = isinstance(X,scipy.sparse.csr_matrix)
    if is_sparse:
        xbuf = np.zeros((X.shape[1],))
    else:
        xbuf = None

    XW = sparse_sdot(xbuf,W,X,i,is_sparse)
    r = U[u].dot(V[i] + XW)
    for N in xrange(1,max_trials):
        # find j!=i s.t. data[u,j] < data[u,i]
        j = sample_negative_example(num_episodes,vals,indices,begin,end,ix)
        XW = sparse_sdot(xbuf,W,X,j,is_sparse)
        if r - U[u].dot(V[j] + XW) < 1:
            # found a violating pair
            return j,N
    # no violating pair found after max_trials, give up
    return -1,max_trials

cdef sparse_sdot(np.ndarray[np.float_t,ndim=1] xbuf,
                 np.ndarray[np.float_t,ndim=2] W,
                 X,
                 i,
                 is_sparse):

    cdef np.ndarray[np.float_t,ndim=1] XW

    if is_sparse:
        # TODO: surely there's something built in to do this...
        for ix in xrange(X.indptr[i],X.indptr[i+1]):
            xbuf[X.indices[ix]] = X.data[ix]
        XW = xbuf.dot(W)
        for ix in xrange(X.indptr[i],X.indptr[i+1]):
            xbuf[X.indices[ix]] = 0
    else:
        XW = X[i].dot(W)
    return XW