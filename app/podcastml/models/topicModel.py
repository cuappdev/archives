import gensim
from stop_words import get_stop_words

class TopicModel:
    """
    Topic model for episodes. Uses latent dirichlet allocation.
    """
    episode_model = None
    episode_dictionary = None
    series_dictionary = None
    
    def _series_summary(self, series):
        pass
    
    def _corpus_from_documents(self, docs):
        for doc in documents:
            texts.append([word for word in document.lower().split() if word not in stop_words])
        dictionary = gensim.corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        return corpus
    
    def _episode_corpus(self, episodes):
        """
        Preprocesses episodes and creates a gensim corpus.
        """
        stop_words = get_stop_words("en")
        texts = []
        documents = [e.summary for e in episodes]
        return self._corpus_from_documents(documents)
    
    def _series_corpus(self, series):
        """
        Finds all episodes in a series, preprocesses their descriptions, and creates a gensim corpus.
        """
        stop_words = get_stop_words("en")
        texts = []
        documents = [self._series_summary(s) for s in series]
        return self._corpus_from_documents(documents)
    
    def __init__(self, episodes, series, n_tags):
        """
        Creates a topic model for a collection of episodes.
        Can be accessed using bracket notation.
        """
        episode_corpus = self._episode_corpus(episodes)
        series_corpus = self._series_corpus(series)
        self.episode_model = gensim.models.LdaModel(corpus, num_topics=n_tags)
        self.series_model = gensim.models.LdaModel(corpus, num_topics=n_tags)
        
    def _run_model_on_bow(self, model, bow):
        if model is not None:
            topic_dist = model[bow]
            sorted_topic_dist = sorted(topic_dist, key=lambda t:t[1], reverse=True)
            return sorted_topic_dist[0][0]
        return None
        
    def top_tag_for_episode(self, episode):
        """
        Uses the topic model for episodes to grab the top tag for an episode.
        """
        bow = self.episode_dictionary.doc2bow(episode.summary)
        self._run_model_on_bow(self, self.episode_model, bow)
            
    def top_tag_for_series(self, series):
        """
        Uses the topic model for series to grab the top tag for a series.
        """
        bow = self.series_dictionary.doc2bow(self._series_summary(series))
        self._run_model_on_bow(self, self.series_model, bow)